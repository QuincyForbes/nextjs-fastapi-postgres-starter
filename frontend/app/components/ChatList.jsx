import React, { forwardRef } from "react";

const ChatList = forwardRef(({ chats, currentChat, setCurrentChat, fetchChatMessages, messages }, ref) => {
  return (
    <ul ref={ref} className="space-y-2 overflow-y-auto flex-1">
      {chats.map((chat) => (
        <li
          key={chat}
          className={`p-3 rounded-lg cursor-pointer transition-all text-white text-center hover:bg-gray-800 ${
            currentChat === chat ? "bg-blue-600" : ""
          }`}
          onClick={() => {
            setCurrentChat(chat);
            if (!messages[chat]) fetchChatMessages(chat);
          }}
        >
          Chat {chat}
        </li>
      ))}
    </ul>
  );
});

export default ChatList;
