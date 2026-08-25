# GitHub Copilot Instructions — Flask Sudoku Refactoring Project

## Project Goal

This project is for Udacity's **Refactoring Legacy Code with Copilot** project.

The goal is to refactor the existing legacy Python Sudoku application into a clean, maintainable, and modern Flask web application while preserving working existing behavior.

Do not unnecessarily rewrite working code. Inspect and understand existing code before modifying it.

## Required Technologies

Use the existing project technology wherever possible.

The target application should use:

* Python 3
* Flask
* HTML5
* CSS3
* Vanilla JavaScript
* pytest for Python testing
* Browser localStorage for persistent Top 10 scores

Do not introduce React, Vue, Angular, or another frontend framework unless explicitly requested.

Do not introduce unnecessary dependencies.

## Development Approach

Before making significant changes:

1. Inspect the existing implementation.
2. Explain the current behavior.
3. Identify problems or legacy patterns.
4. Propose the intended changes.
5. Make changes incrementally.
6. Run the test suite after each significant change.
7. Fix regressions before continuing.

Do not rewrite the entire application at once.

Prefer small, understandable changes over large generated replacements.

## Code Quality

Follow modern Python development practices.

Code should:

* Follow PEP 8 conventions.
* Use meaningful variable and function names.
* Use type hints where they improve clarity.
* Keep functions focused on a single responsibility.
* Avoid duplicated logic.
* Avoid unnecessary global mutable state.
* Include comments where logic is not self-explanatory.
* Use consistent error handling.
* Validate user input appropriately.
* Separate application logic from Flask route handling.

Keep the implementation simple and maintainable.

## Application Structure

Organize the application into logical, reusable components where appropriate.

Separate responsibilities such as:

* Sudoku puzzle generation
* Sudoku solving
* Sudoku validation
* Unique-solution verification
* Game-related logic
* Flask routes
* Frontend interaction
* Styling

Do not place all Sudoku business logic directly inside Flask route functions.

Do not create unnecessary abstractions or modules when a simpler structure is sufficient.

## Sudoku Requirements

The completed application must provide a working 9×9 Sudoku game.

Every generated puzzle must have **exactly one valid solution**.

Puzzle generation must verify uniqueness rather than assuming that a valid puzzle has only one solution.

Use a solution-counting algorithm where necessary to distinguish between:

* No solution
* Exactly one solution
* Multiple solutions

## Difficulty Levels

Support three difficulty levels:

* Easy
* Medium
* Hard

Difficulty must affect how many cells are initially prefilled.

Reasonable clue ranges may be used, for example:

* Easy: approximately 40–45 clues
* Medium: approximately 32–38 clues
* Hard: approximately 24–30 clues

Maintaining a unique solution is more important than reaching an exact clue count.

## Cell Behavior

Original puzzle clues must be locked and must not be editable by the player.

Player-entered cells should remain editable while the game is active.

Cells filled using the Hint feature must become locked.

The UI should visually distinguish relevant cell states when appropriate.

## Validation

Provide immediate feedback for invalid Sudoku moves.

Validation should detect conflicts involving:

* Rows
* Columns
* 3×3 boxes

Invalid or conflicting entries should receive clear visual feedback.

Do not reveal the complete solution simply because the player makes an invalid move.

## Check Feature

The **Check** button must:

* Examine player-entered values.
* Identify incorrect entries.
* Highlight incorrect cells clearly.
* Leave correct entries unchanged.
* Avoid changing locked cells.
* Not automatically solve the puzzle.

## Hint Feature

The **Hint** button must:

1. Select an appropriate empty cell.
2. Fill that cell with its correct solution value.
3. Lock the hinted cell.
4. Visually distinguish it when appropriate.
5. Increase the game's hint count.

A hint must not overwrite original clues or existing player entries.

## Puzzle Completion

A game is complete only when the entire board is correctly solved.

When the player completes the puzzle:

* Detect successful completion.
* Stop the timer.
* Display a congratulatory completion message.
* Allow the player's score to be recorded.
* Prevent duplicate score submissions for the same completed game.

## Timer

Provide a game timer.

The timer should:

* Start when a new game begins.
* Reset when another game starts.
* Update while the game is active.
* Stop when the puzzle is successfully completed.
* Display elapsed time clearly.

## Top 10 Scores

Maintain a **Top 10** scoreboard.

Each completed score should include:

* Player name
* Completion time
* Difficulty
* Number of hints used

Store the scoreboard using browser **localStorage** so that scores persist after page refreshes and between browser sessions.

Scores should be ordered appropriately by completion time, and only the best 10 should be retained.

Handle missing or malformed localStorage data safely.

Do not use a server-side database as a replacement for the required localStorage scoreboard.

## User Interface

The application must work cleanly on desktop and mobile devices.

The UI must include:

* Sudoku grid
* Difficulty selector
* New Game control
* Hint button
* Check button
* Timer
* Dark mode toggle
* Completion feedback
* Top 10 scoreboard

The Sudoku grid must remain aligned without visible layout shifts.

## 3×3 Grid Styling

The nine 3×3 Sudoku sections should have alternating visual styling.

The alternating styling must:

* Clearly distinguish neighboring 3×3 sections.
* Remain stable as cell values change.
* Work in both light and dark modes.
* Preserve readable contrast.
* Avoid layout shifts.

Prefer reusable CSS classes or calculated styling instead of unnecessary inline styles.

## Light and Dark Modes

Support both light and dark themes.

When changing themes:

* Update the complete application UI.
* Keep text readable.
* Keep controls readable.
* Preserve Sudoku grid boundaries.
* Preserve alternating 3×3 section styling.
* Keep validation feedback distinguishable.
* Avoid layout shifts.

CSS custom properties should be preferred where they simplify theme management.

## Responsive Design

The application should scale smoothly between desktop and mobile layouts.

On smaller screens:

* The Sudoku grid should fit within the viewport.
* Horizontal scrolling should be avoided.
* Controls should wrap or resize appropriately.
* Text should remain readable.
* Sudoku cells should remain usable.
* Timer and important game information should remain visible.

## Accessibility

Use reasonable accessibility practices, including:

* Semantic HTML where possible.
* Clear labels.
* Keyboard-accessible controls.
* Visible focus states.
* Readable color contrast.
* Accessible status and feedback messages where practical.

Do not rely only on color when an additional accessible indication can reasonably be provided.

## Testing Requirements

Use **pytest** as the Python testing framework.

Testing must be established **before refactoring the existing application**.

Before changing legacy application behavior:

1. Inspect the current code.
2. Set up the baseline testing framework.
3. Run the baseline tests.
4. Confirm and document their results.

After every significant refactor or feature addition:

1. Run the complete test suite.
2. Investigate failures.
3. Fix regressions before continuing.

Never delete or weaken a legitimate test merely to make the test suite pass.

Tests should eventually cover important logic such as:

* Sudoku board validity
* Solver behavior
* Unique-solution detection
* Puzzle generation
* Difficulty handling
* Move validation
* Hint behavior
* Completion detection
* Important Flask routes

Additional frontend behavior may be tested where practical.

## Responsible Copilot Usage

GitHub Copilot is an assistant, not the final authority on implementation decisions.

For generated suggestions:

* Review the proposed code before accepting it.
* Check that it matches project requirements.
* Reject suggestions that introduce unnecessary complexity.
* Reject suggestions that violate the architecture or requirements.
* Modify suggestions when a simpler or safer solution is available.
* Test generated code before relying on it.

Do not accept generated code blindly.

At least one Copilot suggestion should be explicitly evaluated, rejected, or modified when appropriate, with the reasoning documented for the project evidence.

## Copilot Workflow

Use the appropriate Copilot interaction mode for each task.

For example:

* Use Ask/Plan for understanding and planning.
* Use Edit for controlled code changes.
* Use Agent when coordinated changes across multiple files are genuinely useful.
* Use code completion for small implementation details.

Before large modifications, Copilot should explain the intended approach.

## Scope

Focus first on all functionality required by the Udacity project rubric.

Do **not** implement optional standout features yet, including:

* Number-usage tracking
* Visual Sudoku solver animation
* `prompts.json`

Optional features should only be considered after all required functionality works correctly and all tests pass.

## Important Rule

Preserve working behavior while refactoring.

Do not make unrelated changes.

When uncertain about an architectural or functional decision, explain the alternatives before modifying the application.
