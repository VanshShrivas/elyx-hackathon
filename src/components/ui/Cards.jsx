import React from "react";

// Card wrapper
export function Card({ children, className = "" }) {
  return (
    <div className={`bg-white shadow rounded-xl p-4 ${className}`}>
      {children}
    </div>
  );
}

// Card header
export function CardHeader({ children, className = "" }) {
  return (
    <div className={`mb-2 ${className}`}>
      {children}
    </div>
  );
}

// Card title
export function CardTitle({ children, className = "" }) {
  return (
    <h3 className={`text-lg font-semibold text-gray-800 ${className}`}>
      {children}
    </h3>
  );
}

// Card content
export function CardContent({ children, className = "" }) {
  return (
    <div className={`text-gray-700 ${className}`}>
      {children}
    </div>
  );
}
