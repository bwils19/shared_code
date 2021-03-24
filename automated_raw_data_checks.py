"""
Created on 03/15/21

@author: bwilson
"""

from datetime import timedelta
from datetime import datetime as dt
import datetime
import pandas as pd
import numpy as np
import pyathena
from pyathena import connect
import statistics
import boto3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.transforms as mtransforms
import matplotlib.transforms as transforms
import matplotlib.ticker as ticker

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders

import sys
import os
import io


class RawDataChecks:
	def __init__(self):

		self.key = aws_key
		self.secret = aws_secret

		self.fs = s3fs.S3FileSystem()
		self.sns = boto3.client('sns', region_name='us-east-1')
		self.staging_dir = s3_staging_loc
		self.region = 'us-east-1'

		self.bucket = main_bucket
		self.prefix = bucket_prefix
		self.s3 = boto3.resource('s3')

		# I would like to see the past 2 weeks worth of data
		self.date = dt.today().strftime('%Y-%m-%d')
		date_pull = datetime.datetime.now() - datetime.timedelta(days=14)
		self.date_pull = date_pull.date()

		self.date_dict = {'date': self.date_pull}

		self.raw_count_query = f"""select date, count(distinct id) as distinct_id,
								count(id) as count_id
								from brandon.raw_data
								where date > '{self.date_pull}'
								group by date
								order by date"""

		self.raw_missing_field1 = f"""select date, count(*) as count,
								count(case when field1 is null then 1 else null end) as count_missing
								from brandon.raw_data
								where date > '{self.date_pull}'
								group by date
								order by 1 asc
								"""

	def data_checks(self):

		# Get distinct and total counts from tables
		# print the query before it runs so I know what is being pulled from sql
		print(self.raw_count_query)
		df = self.query_runner(self.raw_count_query)
		print(self.raw_missing_field1)
		df_missing = self.query_runner(self.raw_missing_field1)

		# add a % missing value column to the sql pull
		df_missing['pct_missing'] = (
					(df_missing['count_missing'] / df_missing['count']) * 100)

		# Get the bucket file count and sizes
		bucket_list = []
		client = boto3.client('s3')
		s3 = boto3.resource('s3')
		result = client.list_objects(Bucket=self.bucket, Prefix=self.prefix, Delimiter='/')
		for o in result.get('CommonPrefixes'):
			b = o.get('Prefix')
			b = b[-11:-1]
			b = datetime.datetime.strptime(b, '%Y-%m-%d').date()
			bucket_list.append(b)
		date_list = []

		start_dt = bucket_list[0]
		end_dt = bucket_list[-1]
		for dt in self.daterange(start_dt, end_dt):
			date_list.append(dt.strftime("%Y-%m-%d"))

		df_file_size = pd.DataFrame()
		for d in date_list:
			df1 = pd.DataFrame()
			prefix = f'bucket_prefix/date={d}'
			files = []
			buck = s3.Bucket(self.bucket)
			for obj in buck.objects.filter(Prefix=prefix):
				objsize = obj.size / 1024 / 1024
				files.append(objsize)

			# get the average file size
			average_size = statistics.mean(files)
			df1 = pd.DataFrame({
				'date': d,
				'number_of_files': len(files),
				'ave_file_size': average_size}, index=[0])
			df_file_size = df_file_size.append(df1)

		self.plot_results(df, df_missing, df_file_size)

	def daterange(self, date1, date2):
		for n in range(int((date2 - date1).days) + 1):
			yield date1 + timedelta(n)

	def query_runner(self, query):
		cursor = connect(s3_staging_dir=self.staging_dir, region_name=self.region).cursor()

		# Sometimes the sql query would get stuck, so I added a try and a timeout if it did.
		trys = 0
		while trys <= 5:
			try:
				cursor.execute(query, self.date_dict)
				break
			except Exception as e:
				trys += 1
				if trys == 6:
					print('     [FAILURE] -- Athena trys exceeded limit. Exiting program.')
					print(e)
					exit()
				print('Athena Error, trying again...')

		df = cursor.fetchall()
		df = pd.DataFrame(df)
		column_names = [item[0] for item in cursor.description]
		df.columns = column_names
		return df

	def plot_results(self, df_plot, df_missing, df_file_size):

		plt.style.use('ggplot')
		fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

		# Raw Data counts
		ax1.set_xlabel('Date')
		ax1.set_ylabel('distinct')
		ax1.set_xticklabels(df_plot.date, rotation=45, fontsize=8)
		ln1 = ax1.plot(df_plot.date, df_plot.distinct_id, color='C0', label='distinct')

		ax1 = ax1.twinx()
		ax1.set_ylabel('count')
		ln2 = ax1.plot(df_plot.date, df_plot.count_id, color='C1', label='total count')
		lns = ln1 + ln2
		labs = [l.get_label() for l in lns]
		ax1.legend(lns, labs)
		ax1.set_xlabel("Date")
		ax1.set_title('ID counts')

		# mising value percentage

		ax2.set_xlabel('Date')
		ax2.set_ylabel('percent missing')
		ax2.plot(df_missing.date, df_missing.pct_missing, color='C1', label='distinct count')

		ax2.set_xticklabels(df_missing.date, rotation=45, fontsize=8)

		ax2.set_title('Value fill rate percent')

		ax3.xaxis.set_major_locator(ticker.MaxNLocator(15))
		ax3.tick_params(axis='x', labelrotation=45)
		ax3.plot(df_file_size.date, df_file_size.number_of_files, label="Number of files")

		ax4.xaxis.set_major_locator(ticker.MaxNLocator(15))
		ax4.tick_params(axis='x', labelrotation=45)
		ax4.plot(df_file_size.date, df_file_size.ave_file_size, label="Average file size")

		ax3.set_title("Number of files")
		ax4.set_title("Average file size (MB)")

		ax3.set_ylabel("Number of files")
		ax3.set_xlabel("Date")
		ax4.set_ylabel("Average file size (MB)")
		ax4.set_xlabel("Date")

		fig.suptitle("Raw Data", fontsize=16)
		plt.subplots_adjust(hspace=.5, wspace=.27, top=.88, bottom=.11, left=0.065, right=0.965)
		plt.show()

		with pd.ExcelWriter(f"raw_counts_{self.date}.xlsx") as writer:
			df_plot.to_excel(writer, sheet_name='counts')

		canvas = FigureCanvasAgg(fig)
		imdata = io.BytesIO()
		canvas.print_png(imdata)

		# Email results along with the excel file of the raw data in case i want to look at it more in depth
		self.send_daily_report_ses(fig)

	def send_daily_report(self, fig):

		fig.savefig(f"plot_{self.date}.png")
		message = f"raw data counts from data set, distinct and total id count results for {self.date}"

		body_html = """\
					<html>
					<head></head>
					<body>
					<h4>{message}</h4>
					</body>
					</html>
					""".format(message=message)

		sender = " Brandon Wilson <brandonlwilson19@gmail.com>"
		recipients = ['brandonlwilson19@gmail.com']

		aws_region = "us-east-1"
		subject = f"raw data id counts for {self.date}"
		body_text = message
		charset = "utf-8"

		client = boto3.client('ses', region_name=aws_region)
		msg = MIMEMultipart('mixed')
		msg['Subject'] = subject
		msg['From'] = sender

		msg_body = MIMEMultipart('alternative')

		textpart = MIMEText(body_text.encode(charset), 'plain', charset)
		htmlpart = MIMEText(body_html.encode(charset), 'html', charset)

		msg_body.attach(textpart)
		msg_body.attach(htmlpart)

		fp = open(f"plot_{self.date}.png", 'rb')
		msgimage = MIMEImage(fp.read())
		fp.close()
		msg.attach(msgimage)
		msg.attach(msg_body)

		part = MIMEBase('application', "octet-stream")
		part.set_payload(open(f"raw_counts_{self.date}.xlsx", "rb").read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="raw_counts.xlsx"')
		msg.attach(part)

		try:
			# Provide the contents of the email.
			for p in recipients:
				msg['To'] = p
				response = client.send_raw_email(
					Source=sender,
					Destinations=[
						p
					],
					RawMessage={
						'Data': msg.as_string(),
					}
				)
		# Display an error if something goes wrong.
		except ClientError as e:
			print(e.response['Error']['Message'])
		else:
			print("Email sent! Message ID:"),
			print(response['MessageId'])


def main():

	m = RawDataChecks()
	m.data_checks()


if __name__ == '__main__':
	main()
