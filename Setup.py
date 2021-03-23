from typing import Dict, List
import requests
import json
import os, sys
from rich.console import Console
from rich.progress import track
console = Console()

class Setup :
	def __init__(self) -> None :
		self.urls: Dict[str, str] = {}
		try :
			os.mkdir("files")
		except :
			pass

	def load(self,dictionary: Dict[str, str]) -> None :
		self.urls = dictionary

	def loadJson(self,fileDir: str) -> None :
		with open(fileDir) as jsonFile :
			self.urls = json.load(jsonFile)
	
	def startDownload(self) -> None :
		urls: Dict[str, str] = self.urls
		for fileType in urls :
			for file in urls[fileType] :
				console.log( f"Starting download for {file['name']}......", style='Green')
				r = requests.get(file["url"], stream = True)
				with open(f"files/{ file['name'] }.{ fileType }","wb") as File: 
					
					for chunk in track(r.iter_content(chunk_size=1024), description=f"[yellow]Downloading {file['name']}......", total=(int(r.headers.get('Content-Length'))/1024)): 
						if chunk:
							File.write(chunk) 
					else:
						console.log(f"Downloded {file['name']}", style='bold green')
		else:
			console.log("All downloads finished", style='green bold')
			installStuff: bool = console.input("Do you also want to install all the files? [Y/N] : ").strip().lower() in ["y", "yes"]
			if installStuff:
				self.install()
			runCommands: bool = console.input("Do you also want to run the additional commands? [Y/N] : ").strip().lower() in ["y", "yes"]
			if runCommands:
				self.extraStuff()
			console.log('Completed!', style='bold green')
		
	def install(self):
		allFiles: List[str] = os.listdir('files')
		with console.status("[bold green]Installing applications...") as status:
			for i in allFiles:
				os.system(f'.\\files\\{i}')
				status.update()
			else:
				console.log("Installed all apps", style='bold green')
		
	def extraStuff(self):
		with open("./.vscode/extensions.json", 'r') as file:
			commands = json.loads(file.read())["recommendations"]
		with console.status("[bold green]Running additional commands....") as status:
			for command in commands:
				command:str = "code --install-extension " + command
				os.system(command)
	

if __name__ == "__main__":
	s: Setup = Setup()
	args: list = sys.argv
	# console.log()

	if len(args) > 1 :

		if args[1] == '-test':
			s.extraStuff()
			sys.exit()

		if not args[1].endswith('.json'):
			console.print("Invalid urls file extension, only json files are supported", style='red bold')
			sys.exit()
		try :
			s.loadJson(args[1])
			s.startDownload()
		except FileNotFoundError:
			console.print(f'No file named {args[1]}', style='red bold')
	else :
		try :
			s.loadJson("urls.json")
			s.startDownload()
		except Exception as e:
			console.print('An Error occured')
			console.print(e)

