from typer import Argument, Option, Typer
from terminal_bench.cli.wizard import Wizard, Colors
from terminal_bench.handlers.trial_handler import TaskDifficulty
from pathlib import Path
from typing import Annotated

tasks_app = Typer(no_args_is_help=True)


CATEGORIES = [
    {
        "category": "system-administration",
        "name": "System/Environment Setup & Configuration",
        "description": "Tasks involving OS-level configuration, user management, package management, processes, or installing, configuring, and bringing up services, networks, and environments.",
    },
    {
        "category": "build-and-dependency-management",
        "name": "Build / Compilation / Dependency Management",
        "description": "Tasks that compile code, manage dependencies, build components.",
    },
    {
        "category": "data-processing",
        "name": "Data / File Processing / ETL / Scripting",
        "description": "Tasks that transform, parse, filter, aggregate datasets or files and directories and generate derived output.",
    },
    {
        "category": "games",
        "name": "Interactive / Simulation Tasks / Games",
        "description": "Tasks centered on game-like or simulated environments, interactive puzzles, or simulation games that run in the terminal.",
    },
    {
        "category": "software-engineering",
        "name": "Software-engineering",
        "description": "Tasks focused on developing or testing features and algorithms, fixing bugs and improving/optimizing an existing feature, implementing tests, or maintaining software projects.",
    },
    {
        "category": "machine-learning",
        "name": "Machine Learning / Model Training / Inference",
        "description": "Tasks requiring training, fine-tuning, running inference, or evaluating machine learning models, including dependency setup,running training loops, and managing data pipelines for ML tasks.",
    },
    {
        "category": "debugging",
        "name": "Debugging / Repair / Fixing Tasks",
        "description": "Tasks that require identifying, diagnosing, and fixing errors in scripts, codebases, or system configurations.",
    },
    {
        "category": "security",
        "name": "Security / Cryptography / Vulnerability Demonstration",
        "description": "Tasks related to cryptography, authentication, permissions, penetration-style tests, exploit, validate vulnerabilities, reverse engineering or security configuration.",
    },
    {
        "category": "scientific-computing",
        "name": "Scientific-computing",
        "description": "Tasks using scientific libraries or workflows, such as numerical computation, simulations, or domain-specific research code.",
    },
]


class SnorkelWizard(Wizard):
    _TEMPLATE_DIR = Path(__file__).parent.parent.parent / "template-task"

    def _show_welcome(self, color: str) -> None:
        self._print_with_color(
            r"""
#####################################################################
#  _____                   _             _     ______________       #
# |_   _|__ _ __ _ __ ___ (_)_ __   __ _| |   ||            ||      #
#   | |/ _ \ '__| '_ ` _ \| | '_ \ / _` | |   || >          ||      #
#   | |  __/ |  | | | | | | | | | | (_| | |   ||            ||      #
#   |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|_|   ||____________||      #
#   ____                  _                   |______________|      #
#  | __ )  ___ _ __   ___| |__                 \\############\\     #
#  |  _ \ / _ \ '_ \ / __| '_ \                 \\############\\    #
#  | |_) |  __/ | | | (__| | | |                 \      ____    \   #
#  |____/ \___|_| |_|\___|_| |_|                  \_____\___\____\  #
#                                                                   #
#####################################################################
          """,
            color=color,
        )
        self._print_with_color(
            "=== Snorkel Terminal-Bench Tasks ===",
            color=color + Colors.BOLD,
        )
        self._print_with_color(
            "This wizard will help you create a new task for the Snorkel Terminal-Bench Tasks project.",
            color=color,
            end="\n\n",
        )

    def _get_category(self, color: str) -> None:
        # Show difficulty rubric
        self._print_with_color(
            "Task Category",
            color=Colors.BOLD + Colors.YELLOW,
        )
        self._print_with_color(
            "Select the category that best describes the task:\n",
            color=color,
        )

        for i, category_dict in enumerate(CATEGORIES):
            category = category_dict["category"]
            name = category_dict["name"]
            description = category_dict["description"]
            self._print_with_color(
                f"{i + 1}. {name} (category: {category}): ",
                color=color + Colors.BOLD,
            )
            self._print_with_color(
                f"  {description}",
                color=color,
            )
        self._print_with_color(
            "",
            color=color,
        )

        while True:
            category_number = (
                self._input_with_color(
                    f"Select the category that best describes the task [1-{len(CATEGORIES)}]: ",
                    color,
                )
                .lower()
                .strip()
            )

            if category_number in [str(i + 1) for i in range(len(CATEGORIES))]:
                self._category = CATEGORIES[int(category_number) - 1]["category"]
                break

            self._print_with_color(
                f"Please enter a valid category number [1-{len(CATEGORIES)}]",
                color=Colors.RED,
            )

    def _create_files(self, color: str) -> None:
        super()._create_files(color)
        self._copy_template_file(".dockerignore")


@tasks_app.command()
def create(
    task_id: Annotated[
        str | None,
        Argument(help="Task ID (e.g. hello-world)."),
    ] = None,
    tasks_dir: Annotated[
        Path,
        Option(help="The path in which to create the new task."),
    ] = Path("tasks"),
    instruction: Annotated[
        str | None,
        Option(help="Task instruction."),
    ] = None,
    interactive: Annotated[
        bool | None,
        Option(help="Whether the solution is interactive."),
    ] = None,
    category: Annotated[
        str | None,
        Option(help="Task category."),
    ] = None,
    tags: Annotated[
        list[str] | None,
        Option(
            "--tag",
            "-t",
            help="Task tags. Can be set multiple times to add multiple tags.",
        ),
    ] = None,
    difficulty: Annotated[
        TaskDifficulty | None,
        Option(help="Task difficulty."),
    ] = None,
    expert_time_estimate_min: Annotated[
        int | None,
        Option(help="Expert time estimate in minutes."),
    ] = None,
    junior_time_estimate_min: Annotated[
        int | None,
        Option(help="Junior engineer time estimate in minutes."),
    ] = None,
):
    """Starts an interactive wizard to create a new task."""
    wizard = SnorkelWizard(
        tasks_dir=Path("tasks"),
        task_id=task_id,
        instruction=instruction,
        interactive=interactive,
        name="anonymous",
        email="anonymous",
        category=category,
        tags=tags,
        difficulty=difficulty,
        expert_time_estimate_min=expert_time_estimate_min,
        junior_time_estimate_min=junior_time_estimate_min,
    )
    wizard.run()
