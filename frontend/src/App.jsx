import { useEffect, useState } from "react";

function App() {
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [students, setStudents] = useState([]);
  const [projects, setProjects] = useState([]);
  const [generatedTeam, setGeneratedTeam] = useState(null);
  const [teamLoading, setTeamLoading] = useState(false);
  const [whatIfSkill, setWhatIfSkill] = useState(8);
  const [whatIfResult, setWhatIfResult] = useState(null);
  const [skillGapResult, setSkillGapResult] = useState(null);
  const [matchResults, setMatchResults] = useState(null);
  const [teamSkillGapResult, setTeamSkillGapResult] = useState(null);
const [teamGapLoading, setTeamGapLoading] = useState(false);
const [dashboardStats, setDashboardStats] = useState({
  students: 0,
  projects: 0,
  teams: 0,
  skills: 0,
});

  useEffect(() => {
    // Backend status
    fetch("http://127.0.0.1:8000/")
      .then((response) => response.json())
      .then((data) => {
        setBackendStatus(data.message);
      })
      .catch(() => {
        setBackendStatus("Backend connection failed");
      });

    // Students
    fetch("http://127.0.0.1:8000/students")
      .then((response) => response.json())
      .then((data) => {
        setStudents(data);
      })
      .catch((error) => {
        console.error("Students fetch error:", error);
      });

    // Projects
    fetch("http://127.0.0.1:8000/projects")
      .then((response) => response.json())
      .then((data) => {
        setProjects(data);
      })
      .catch((error) => {
        console.error("Projects fetch error:", error);
      });
  }, []);

  fetch("http://127.0.0.1:8000/dashboard-stats")
  .then((response) => response.json())
  .then((data) => {
    setDashboardStats(data);
  })
  .catch((error) => {
    console.error("Dashboard stats error:", error);
  });

  return (
    <div className="app">
      <header className="header">
        <h1>TeamIQ</h1>
        <p>
          AI-Based Project Team Formation and Skill Intelligence System
        </p>
      </header>

      <main className="dashboard">
       <div className="dashboard-title">
  <div>
    <h2>TeamIQ Dashboard</h2>
    <p>AI-powered student skill and project team intelligence</p>
  </div>
</div>

        {/* Backend Status */}
        <div className="status-card">
          <div className="summary-grid">
  <div className="summary-card">
    <h3>Total Students</h3>
    <p>{dashboardStats.students}</p>
  </div>

  <div className="summary-card">
    <h3>Total Projects</h3>
    <p>{dashboardStats.projects}</p>
  </div>

  <div className="summary-card">
    <h3>Generated Teams</h3>
    <p>{dashboardStats.teams}</p>
  </div>

  <div className="summary-card">
    <h3>Skills Tracked</h3>
    <p>{dashboardStats.skills}</p>
  </div>
</div>
  <div>
    <h3>System Status</h3>
    <p className="status">{backendStatus}</p>
  </div>

  <div className="status-indicator">
    ● API Connected
  </div>
</div>

        {/* Students */}
        <section>
          <h2>Students</h2>

          <div className="student-grid">
            {students.length === 0 ? (
              <p>No students found.</p>
            ) : (
              students.map((student) => (
                <div className="student-card" key={student.id}>
                  <h3>{student.name}</h3>

                  <p>
                    <strong>Email:</strong> {student.email}
                  </p>

                  <p>
                    <strong>Role:</strong> {student.role}
                  </p>

                  <p>
                    <strong>Roll Number:</strong> {student.roll_number}
                  </p>

                  <p>
                    <strong>Branch:</strong> {student.branch}
                  </p>

                  <p>
                    <strong>Semester:</strong> {student.semester}
                  </p>

                  <p>
                    <strong>CGPA:</strong> {student.cgpa}
                  </p>
                  <p><strong>Availability:</strong> {student.availability_hours} hrs/week</p>
                </div>
              ))
            )}
          </div>
        </section>
        {/* Student-Project Match */}
<div className="feature-card">
  <h3>Student-Project Matching</h3>

  <p>
    Calculate how well students match the project requirements.
  </p>

  <button
    onClick={() => {
      fetch("http://127.0.0.1:8000/project-matches/1")
        .then((response) => response.json())
        .then((data) => {
          setMatchResults(data);
        })
        .catch((error) => {
          console.error("Match results error:", error);
        });
    }}
  >
    Calculate Match
  </button>

  {matchResults && (
    <div>
      <h4>Match Results</h4>

      {matchResults.matches.map((match) => (
        <div key={match.student_id}>
          <p><strong>Name:</strong> {match.name}</p>
          <p>
            <strong>Student ID:</strong> {match.student_id}
          </p>

          <p>
            <strong>Roll Number:</strong> {match.roll_number}
          </p>

          <p>
            <strong>Match Score:</strong> {match.match_score}%
          </p>

          <hr />
        </div>
      ))}
    </div>
  )}
</div>

        {/* Features */}
        <section className="feature-grid">

          {/* Projects */}
          <div className="feature-card">
            <h3>Projects</h3>

            {projects.length === 0 ? (
              <p>No projects found.</p>
            ) : (
              projects.map((project) => (
                <div key={project.id}>
                  <h4>{project.title}</h4>

                  <p>{project.description}</p>

                  <p>
                    <strong>Team Size:</strong> {project.team_size}
                  </p>

                  <p>
                    <strong>Status:</strong> {project.status}
                  </p>
                </div>
              ))
            )}
          </div>

          {/* AI Team Formation */}
          <div className="feature-card">
            <h3>AI Team Formation</h3>

            <p>
              Generate balanced project teams using skill matching.
            </p>

            <button
              onClick={() => {
                setTeamLoading(true);

                fetch("http://127.0.0.1:8000/generate-team/1", {
                  method: "POST",
                })
                  .then((response) => response.json())
                  .then((data) => {
                    setGeneratedTeam(data);
                    setTeamLoading(false);
                  })
                  .catch((error) => {
                    console.error("Team generation error:", error);
                    setTeamLoading(false);
                  });
              }}
            >
              {teamLoading ? "Generating..." : "Generate AI Team"}
            </button>

            {generatedTeam && (
              <div>
                <h4>Generated Team</h4>

                <p>
                  <strong>Team ID:</strong> {generatedTeam.team_id}
                </p>

                <p>
                  <strong>Team Size:</strong> {generatedTeam.team_size}
                </p>

                <p>
                  <strong>Student IDs:</strong>{" "}
                  {generatedTeam.student_ids?.join(", ")}
                </p>
              </div>
            )}
          </div>

          {/* Team Skill Coverage */}
<div className="feature-card">
  <h3>Team Skill Coverage</h3>

  <p>
    Analyze whether the generated team covers the project's required skills.
  </p>

  <button
    onClick={() => {
      setTeamGapLoading(true);

      fetch(
  `http://127.0.0.1:8000/team-skill-gaps/${generatedTeam.team_id}`
)
        .then((response) => response.json())
        .then((data) => {
          setTeamSkillGapResult(data);
          setTeamGapLoading(false);
        })
        .catch((error) => {
          console.error("Team skill gap error:", error);
          setTeamGapLoading(false);
        });
    }}
  >
    {teamGapLoading ? "Analyzing..." : "Analyze Team Coverage"}
  </button>

  {teamSkillGapResult && (
    <div>
      <h4>Team Skill Coverage</h4>

      {Object.entries(teamSkillGapResult.team_skills).map(
        ([skillId, level]) => (
          <p key={skillId}>
            <strong>Skill ID {skillId}:</strong> Level {level}
          </p>
        )
      )}

      <h4>Skill Gaps</h4>

      {teamSkillGapResult.skill_gaps.length === 0 ? (
        <p>No skill gaps found. Team covers all required skills.</p>
      ) : (
        teamSkillGapResult.skill_gaps.map((gap) => (
          <div key={gap.skill_id}>
            <p>
              <strong>{gap.skill_name}</strong>
            </p>

            <p>
              Required: {gap.required_level} | Current: {gap.team_level}
            </p>

            <p>
              Gap: {gap.gap}
            </p>
          </div>
        ))
      )}
    </div>
  )}
</div>

          {/* What-if Simulator */}
          <div className="feature-card">
            <h3>What-if Simulator</h3>

            <p>
              Simulate skill changes and team impact.
            </p>

            <label>
              Python Skill Level: {whatIfSkill}
            </label>

            <br />

            <input
              type="range"
              min="1"
              max="10"
              value={whatIfSkill}
              onChange={(event) => {
                setWhatIfSkill(Number(event.target.value));
              }}
            />

            <br />

            <button
              onClick={() => {
                fetch("http://127.0.0.1:8000/what-if/1/1", {
                  method: "POST",
                  headers: {
                    "Content-Type": "application/json",
                  },
                  body: JSON.stringify({
                    skill_id: 1,
                    new_level: whatIfSkill,
                  }),
                })
                  .then((response) => response.json())
                  .then((data) => {
                    setWhatIfResult(data);
                  })
                  .catch((error) => {
                    console.error("What-if error:", error);
                  });
              }}
            >
              Simulate Change
            </button>

            {whatIfResult && (
              <div>
                <h4>Simulation Result</h4>

                <p>
                  <strong>Simulated Match Score:</strong>{" "}
                  {whatIfResult.simulated_match_score}%
                </p>
              </div>
            )}
          </div>
          {/* Skill Gap Analysis */}
<div className="feature-card">
  <h3>Skill Gap Analysis</h3>

  <p>
    Identify skills that need improvement for the selected project.
  </p>

  <button
    
  onClick={() => {
    fetch(
  `http://127.0.0.1:8000/skill-gaps/${generatedTeam.team_id}/${generatedProject.project_id}`
)
      .then((response) => response.json())
      .then((data) => {
        setSkillGapResult(data);
      })
      .catch((error) => {
        console.error("Skill gap error:", error);
      });
  }}
>
  Analyze Skill Gaps
</button>
{skillGapResult && (
  <div>
    <h4>Skill Gap Result</h4>

    {skillGapResult.skill_gaps.length === 0 ? (
      <p>No skill gaps found.</p>
    ) : (
      skillGapResult.skill_gaps.map((gap) => (
        <div key={gap.skill_id}>
          <p>
            <strong>Skill:</strong> {gap.skill_name}
          </p>

          <p>
            <strong>Required Level:</strong> {gap.required_level}
          </p>

          <p>
            <strong>Current Level:</strong> {gap.team_level}
          </p>

          <p>
            <strong>Gap:</strong> {gap.gap}
          </p>

          <hr />
        </div>
      ))
    )}
  </div>
)}
  
</div>

        </section>
      </main>
    </div>
  );
}

export default App;