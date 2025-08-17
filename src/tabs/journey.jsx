export default function Journey({ data }) {
  if (!data || data.length === 0) {
    return <p className="text-center text-gray-500">Generating Visual Journey....</p>;
  }

  return (
    <div className="space-y-6">
      {data.map((ep) => (
        <div
          key={ep.episode}
          className="border rounded-xl bg-white shadow p-6 hover:shadow-lg transition"
        >
          {/* Title + Date */}
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold text-blue-600">
              Episode {ep.episode}: {ep.title}
            </h2>
            <span className="text-sm text-gray-500">{ep.date_range}</span>
          </div>

          {/* Triggered By + Goal */}
          <p className="mb-2 text-gray-700">
            <span className="font-semibold">Triggered by:</span> {ep.triggered_by}
          </p>
          <p className="mb-4 text-gray-700">
            <span className="font-semibold">Primary Goal Trigger:</span> {ep.primary_goal_trigger}
          </p>

          {/* Persona Before/After */}
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="p-4 bg-red-50 rounded-lg">
              <h3 className="font-semibold text-red-600">Before State</h3>
              <p className="text-sm text-gray-700">{ep.persona_analysis.before_state}</p>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <h3 className="font-semibold text-green-600">After State</h3>
              <p className="text-sm text-gray-700">{ep.persona_analysis.after_state}</p>
            </div>
          </div>

          {/* Friction Points */}
          <div className="mb-4">
            <h3 className="font-semibold text-yellow-600">Friction Points</h3>
            <ul className="list-disc list-inside text-sm text-gray-700">
              {ep.friction_points.map((point, idx) => (
                <li key={idx}>{point}</li>
              ))}
            </ul>
          </div>

          {/* Metrics */}
          <div className="flex gap-6 text-sm text-gray-700 mb-4">
            <p>
              <span className="font-semibold">Response Time:</span>{" "}
              {ep.metrics.response_time}
            </p>
            <p>
              <span className="font-semibold">Time to Resolution:</span>{" "}
              {ep.metrics.time_to_resolution}
            </p>
          </div>

          {/* Outcome */}
          <div className="p-4 bg-blue-50 rounded-lg">
            <h3 className="font-semibold text-blue-600">Final Outcome</h3>
            <p className="text-sm text-gray-700">{ep.final_outcome}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
