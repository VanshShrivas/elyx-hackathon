// import { Card, CardContent } from "@/components/ui/card"; // if shadcn/ui available, else use divs

export default function Visualizer({ data }) {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold mb-4 text-center">Chat Visualizer</h1>

      {/* Loop through months */}
      {data.months.map((month) => (
        <div key={month.month_index} className="bg-white rounded-xl shadow p-4">
          <h2 className="text-xl font-semibold mb-2 text-blue-600">
            {month.month} <span className="text-gray-500 text-sm">({month.theme})</span>
          </h2>

          {/* Weeks timeline */}
          <div className="border-l-2 border-dashed border-gray-300 ml-4 pl-4 space-y-6">
            {month.weeks.map((week) => (
              <div key={week.week} className="relative">
                {/* Timeline dot */}
                <span className="absolute -left-6 top-1 w-4 h-4 bg-blue-400 rounded-full border-2 border-white shadow"></span>

                <h3 className="text-md font-semibold text-gray-700 mb-2">
                  Week {week.week}
                </h3>

                {/* Summary cards for that week */}
                <div className="grid sm:grid-cols-2 gap-4">
                  {week.messages.slice(0, 3).map((msg) => (
                    <div
                      key={msg.id}
                      className={`rounded-lg shadow-sm p-3 text-sm ${
                        msg.role === "member"
                          ? "bg-blue-50 border border-blue-200"
                          : "bg-gray-100 border border-gray-200"
                      }`}
                    >
                      <p className="font-semibold text-gray-700">{msg.author}</p>
                      <p className="truncate">{msg.text}</p>
                      <p className="text-[10px] text-gray-500 mt-1">
                        {msg.timestamp.slice(0, 10)}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
