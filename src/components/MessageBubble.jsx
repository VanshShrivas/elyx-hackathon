export default function MessageBubble({ message }) {
  const isMember = message.role === "member"; // Rohan Patel = member

  return (
    <div className={`flex mb-3 ${isMember ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-xs md:max-w-md px-4 py-2 text-sm shadow-md rounded-2xl relative
          ${isMember 
            ? "bg-blue-500 text-white rounded-br-none"   // You (Rohan Patel)
            : "bg-gray-200 text-gray-900 rounded-bl-none"} // Others
        `}
      >
        {/* Show author only if it's not Rohan Patel */}
        {!isMember && (
          <p className="text-xs font-semibold text-gray-700 mb-1">
            {message.author}
          </p>
        )}

        {/* Text */}
        <p className="whitespace-pre-line">{message.text}</p>

        {/* Timestamp */}
        <p
          className={`text-[10px] opacity-70 mt-1 font-bold ${
            isMember ? "text-right" : "text-left"
          }`}
        >
          {message.timestamp.slice(5, 16)}
        </p>

        {/* Decision (if any) */}
        {message.decision && (
          <div className="mt-2 p-2 text-xs rounded bg-yellow-100 border border-yellow-300">
            <p className="font-semibold">Decision</p>
            <p><b>Action:</b> {message.decision.action}</p>
            <p><b>Reason:</b> {message.decision.reason}</p>
            <p><b>Trigger:</b> {message.decision.trigger}</p>
          </div>
        )}
      </div>
    </div>
  );
}
