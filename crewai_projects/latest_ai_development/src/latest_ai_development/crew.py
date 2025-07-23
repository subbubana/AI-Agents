from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class LatestAiDevelopmentCrew():
    """LatestAiDevelopment crew"""
    def __init__(self):
        # You'll likely use an LLM configured in your .env or directly here
        # For simplicity, we'll assume an LLM is configured globally or passed to agents
        pass

    agents: List[BaseAgent]
    tasks: List[Task]

    manager = Agent(
    role="Project Manager",
    goal="Efficiently manage the crew and ensure high-quality task completion. When using tools, always provide arguments as plain strings, not as dictionaries.",
    backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard.  When delegating work, always follow the tool's input schema exactly.",
    allow_delegation=True,
)

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    @before_kickoff
    def before_kickoff_function(self, inputs):
        print(f"Before kickoff function with inputs: {inputs}")
        return inputs # You can return the inputs or modify them as needed

    @after_kickoff
    def after_kickoff_function(self, result):
        print(f"After kickoff function with result: {result}")
        return result # You can return the result or modify it as needed
    
    

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            manager_agent=self.manager,
            # process=Process.hierarchical # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
