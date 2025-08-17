import MessageBubble from "./MessageBubble";

export default function ChatView({ data }) {
  return (
    <div className="space-y-6">
      {data.months.map((month) => (
        <div
          key={month.month_index}
          className="bg-gray-50 shadow rounded-xl p-4"
        >
          <h2 className="text-xl font-semibold mb-4 border-b pb-2">
            {month.month} –{" "}
            <span className="text-gray-600 italic">{month.theme}</span>
          </h2>

          {month.weeks.map((week) => {
            let lastDate = null;
            return (
              <div key={week.week} className="mb-6">
                <h3 className="text-md font-medium text-gray-700 mb-3">
                  Week {week.week}
                </h3>
                <div className="space-y-3">
                  {week.messages.map((msg) => {
                    const msgDate = msg.timestamp.slice(5, 10); // YYYY-MM-DD
                    const showDate = msgDate !== lastDate;
                    lastDate = msgDate;

                    return (
                      <div key={msg.id}>
                        {/* Date separator */}
                        {showDate && (
                          <div className="flex justify-center my-4">
                            <span className="text-xs font-semibold bg-gray-300 text-gray-800 px-3 py-1 rounded-full">
                              {msgDate}
                            </span>
                          </div>
                        )}
                        <MessageBubble message={msg} />
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}
