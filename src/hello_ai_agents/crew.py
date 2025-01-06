import os
from dotenv import load_dotenv
load_dotenv() 

from langtrace_python_sdk import langtrace
langtrace.init(api_key=os.getenv('LANGTRACE_API_KEY'))

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class HelloAiAgents():
	"""HelloAiAgents crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def aspnet_blog_finder(self) -> Agent:
		return Agent(
			name="ASP.NET Blog Finder",
			role=self.agents_config['aspnet_blog_finder']['role'],
			goal=self.agents_config['aspnet_blog_finder']['goal'],
			backstory=self.agents_config['aspnet_blog_finder']['backstory'],
			verbose=True
		)

	@agent
	def aspnet_content_analyst(self) -> Agent:
		return Agent(
			name="ASP.NET Content Analyst",
			role=self.agents_config['aspnet_content_analyst']['role'],
			goal=self.agents_config['aspnet_content_analyst']['goal'],
			backstory=self.agents_config['aspnet_content_analyst']['backstory'],
			verbose=True
		)

	@agent
	def aspnet_link_curator(self) -> Agent:
		return Agent(
			name="ASP.NET Link Curator",
			role=self.agents_config['aspnet_link_curator']['role'],
			goal=self.agents_config['aspnet_link_curator']['goal'],
			backstory=self.agents_config['aspnet_link_curator']['backstory'],
			verbose=True
		)

	@task
	def blog_discovery_task(self) -> Task:
		return Task(
			description=self.tasks_config['blog_discovery_task']['description'],
			expected_output=self.tasks_config['blog_discovery_task']['expected_output'],
			agent=self.aspnet_blog_finder(),
			output_file='blog_discovery.md'
		)

	@task
	def content_analysis_task(self) -> Task:
		return Task(
			description=self.tasks_config['content_analysis_task']['description'],
			expected_output=self.tasks_config['content_analysis_task']['expected_output'],
			agent=self.aspnet_content_analyst(),
			output_file='content_analysis.md'
		)

	@task
	def link_curation_task(self) -> Task:
		return Task(
			description=self.tasks_config['link_curation_task']['description'],
			expected_output=self.tasks_config['link_curation_task']['expected_output'],
			agent=self.aspnet_link_curator(),
			output_file='link_curation.md'
		)

	@crew
	def aspnet_blog_crew(self) -> Crew:
		"""Creates the ASP.NET blog research crew"""
		discovery = self.blog_discovery_task()
		analysis = self.content_analysis_task()
		curation = self.link_curation_task()

		return Crew(
			agents=[
				self.aspnet_blog_finder(),
				self.aspnet_content_analyst(),
				self.aspnet_link_curator()
			],
			tasks=[
				discovery,
				analysis,
				curation
			],
			verbose=True
		)
