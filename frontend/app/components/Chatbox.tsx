"use client";

import { useState, useRef, useCallback } from "react";
import UserSelector from "./UserSelector";
import ChatList from "./ChatList";
import MessageList from "./MessageList";
import UserNamePrompt from "./UserNameModal";
import { useUsers } from "../hooks/useUsers";
import { useSelectedUser } from "../hooks/useSelectedUser";
import { useChatThreads } from "../hooks/useChatThreads";
import { useChatMessages } from "../hooks/useChatMessages";
import { BASE_URL } from "../api/config";

export default function Chatbox() {
  const { users, refreshUsers } = useUsers();
  const { selectedUser, setSelectedUser, loading } = useSelectedUser();
  const { chats, chatNames, setChats, setChatNames } = useChatThreads(selectedUser);
  const { messages, setMessages, fetchChatMessages } = useChatMessages();
  const [currentChat, setCurrentChat] = useState<number | null>(null);
  const [input, setInput] = useState<string>("");
  const [showUserNameModal, setShowUserNameModal] = useState<boolean>(false);
  const chatListRef = useRef<HTMLUListElement | null>(null);


  const handleNewChat = () => {
    const tempChatId = null;
    setCurrentChat(tempChatId);
    setMessages((prev) => ({
      ...prev,
      [Number(tempChatId)]: null, 
    }));
  };
  

  const sendMessage = useCallback(async () => {
    if (!input.trim() || !selectedUser) return;
  
    const messagePayload = {
      user_id: selectedUser.id,
      message: input,
      thread_id: currentChat || null, 
    };
    
  
    try {
      const res = await fetch(`${BASE_URL}/messages`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(messagePayload),
      });
  
      if (!res.ok) throw new Error("Failed to send message");
  
      const data = await res.json();
      const threadId: number = data.thread_id;
  
      if (!chats.includes(threadId)) {
        setChats((prevChats) => [threadId, ...prevChats]);
        setChatNames((prev) => ({ ...prev, [threadId]: `Chat ${threadId}` }));
        setCurrentChat(threadId);
      }
  
      setMessages((prev) => ({
        ...prev,
        [threadId]: [
          ...(prev[threadId] || []),
          { text: input, sender: "User" },
          {
            text: data.content,
            sender: data.sender_type === "System" ? "System" : "User",
          },
        ],
      }));
  
      setInput("");
    } catch (error) {
      console.error("Error sending message:", error);
    }
  }, [input, selectedUser, currentChat, chats, setChats, setChatNames, setMessages]);

  const handleModalClose = () => {
    setShowUserNameModal(false);
    refreshUsers();
    setCurrentChat(null);
    setMessages({});
    setChats([]);
    setChatNames({});
  };
  
  if (loading) {
    return (
      <div className="h-screen w-full flex items-center justify-center">
        <span className="text-gray-500 text-lg">Loading chat...</span>
      </div>
    );
  }

  return (
    <div className="flex h-screen w-full bg-gray-50 ml-5">
      <div className="w-1/4 bg-gray-900 text-white p-6 flex flex-col space-y-4">
        <button
          className="text-sm bg-blue-500 px-6 py-3 rounded-lg hover:bg-blue-600 transition duration-300 ease-in-out transform hover:scale-105 shadow-md focus:outline-none focus:ring-2 focus:ring-blue-400 w-full"
          onClick={() => setShowUserNameModal(true)}
        >
          + Add User
        </button>

        <div className="flex items-center">
          <div className="flex-1">
            <UserSelector
              users={users ?? []}
              selectedUser={selectedUser}
              setSelectedUser={setSelectedUser}
            />
          </div>
        </div>

        <button
          className={`text-sm px-6 py-3 rounded-lg w-full transition duration-300 ease-in-out transform ${
            chats.length === 0
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-green-500 hover:bg-green-600 hover:scale-105"
          }`}
          onClick={handleNewChat}
          disabled={chats.length === 0}
        >
          + New Chat
        </button>

        <ChatList
          ref={chatListRef}
          chats={chats}
          chatNames={chatNames}
          currentChat={currentChat}
          setCurrentChat={setCurrentChat}
          fetchChatMessages={fetchChatMessages}
          messages={messages}
        />
      </div>

      <div className="w-3/4 flex flex-col p-4 h-screen ml-5">
        <MessageList messages={messages} currentChat={currentChat} />

        <div className="flex mt-4 p-3 border bg-white rounded-lg shadow-md">
          <input
            className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
              }
            }}
            placeholder="Type a message..."
          />
          <button
            className="ml-3 p-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition duration-300 ease-in-out transform hover:scale-105"
            onClick={sendMessage}
            tabIndex={0}
          >
            Send
          </button>
        </div>
      </div>

      {showUserNameModal && (
        <UserNamePrompt
          setSelectedUser={setSelectedUser}
          setShowUserNameModal={handleModalClose}
        />
      )}
    </div>
  );
}
