"use client";

import { useEffect, useRef } from "react";
import { MessageListProps } from "../types/MessageListProps";

export default function MessageList({
  messages,
  currentChat,
}: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!currentChat) return;

    const messagesForCurrent = messages[currentChat];
    if (messagesEndRef.current && messagesForCurrent) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [currentChat, messages]);

  return (
    <div className="flex-1 overflow-y-auto bg-white p-4 border rounded-lg">
      {currentChat ? (
        messages[currentChat] && messages[currentChat].length > 0 ? (
          messages[currentChat].map((msg, index) => {
            const sender = msg.sender || msg.sender_type || "Unknown";
            const isUser = sender === "User";

            return (
              <div
                key={index}
                className={`p-2 my-1 rounded-lg max-w-[75%] ${
                  isUser
                    ? "bg-blue-200 text-left ml-auto"
                    : "bg-gray-200 text-left mr-auto"
                }`}
                style={{ wordWrap: "break-word", whiteSpace: "normal" }}
              >
                <p className="text-xs text-gray-500">
                  {isUser ? "You" : sender}
                </p>
                <p className="text-black">
                  {msg.text || msg.content || "No message content"}
                </p>
              </div>
            );
          })
        ) : (
          <p className="text-gray-500 text-center">No messages yet.</p>
        )
      ) : (
        <p className="text-gray-500 text-center">
          Select a chat to view messages.
        </p>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}
