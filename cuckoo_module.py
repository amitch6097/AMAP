import requests
import os
import sys
import time
import subprocess
import json

class CuckooModule():
	def __init__(self):
		self.cuckoo = subprocess.Popen(["cuckoo"])
		time.sleep(5)	
		self.server = subprocess.Popen(["cuckoo","api","-H","0.0.0.0","-p","8090"])
		time.sleep(5)
		self.submit_url = "http://0.0.0.0:8090/tasks/create/file"
		self.report_url = "http://0.0.0.0:8090/tasks/report"
	def __del__(self):
		self.cuckoo.kill()
		self.server.kill()
	def submit_file(self,filename):
		"""submits a file to the cuckoo api and returns the task id that is used to find that file later"""
				
		with open(filename,"rb") as sample:
			files = {"file":("temp_file_name",sample)}
			request = requests.post(self.submit_url,files=files)
		return request.json()["task_id"]
	def get_report(self,task_id):
		"""submit a task id and returns the report object, if the task is not done or invalid returns None"""
				
		request = requests.post("{}/{}".format(self.report_url,task_id))
		
		if request.status_code == 404:
			return None
		return json.loads(request.text)

if __name__ == "__main__":
	mod = CuckooModule()
	
	task = mod.submit_file("/home/cse498/Desktop/GameSetup.exe")
	while True:
		answer = mod.get_report(task)
		if answer is not None:
			break
	print answer