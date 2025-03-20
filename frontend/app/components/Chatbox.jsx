"use client";

import { useState, useEffect, useRef } from "react";
import UserSelector from "./UserSelector";
import ChatList from "./ChatList";
import MessageList from "./MessageList";
import UserNamePrompt from "./UserNameModal";

export default function Chatbox() {
  const [users, setUsers] = useState(null);
  const [selectedUser, setSelectedUser] = useState(() => {
    try {
      const savedUser = localStorage.getItem("selectedUser");
      return savedUser ? JSON.parse(savedUser) : null;
    } catch (error) {
      console.error("Error parsing selectedUser from localStorage", error);
      return null;
    }
  });
  const [chats, setChats] = useState([]);
  const [chatNames, setChatNames] = useState({});
  const [currentChat, setCurrentChat] = useState(null);
  const [messages, setMessages] = useState({});
  const [input, setInput] = useState("");
  const [showUserNameModal, setShowUserNameModal] = useState(false);
  const chatListRef = useRef(null);

  const fetchUsers = () => {
    fetch("http://127.0.0.1:8000/api/v1/users")
      .then((res) => res.json())
      .then((data) => {
        if (data && data.length === 0) {
          setUsers([]);
        } else {
          setUsers(data);
        }
      })
      .catch(() => setUsers([]));
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  useEffect(() => {
    if (selectedUser) {
      localStorage.setItem("selectedUser", JSON.stringify(selectedUser));
      setChats([]);
      setChatNames({});
      setCurrentChat(null);
      setMessages({});

      fetch(`http://127.0.0.1:8000/api/v1/threads?user_id=${selectedUser.id}`)
        .then((res) => (res.ok ? res.json() : []))
        .then((data) => {
          const threadIds = Array.isArray(data) ? data.map((thread) => thread.id) : [];
          setChats(threadIds.reverse());
          setChatNames(Object.fromEntries(threadIds.map((id) => [id, `Chat ${id}`])));
        })
        .catch(() => setChats([]));
    }
  }, [selectedUser]);

  const fetchChatMessages = async (chatId) => {
    if (!chatId) return;

    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/messages?thread_id=${chatId}`);
      if (!res.ok) throw new Error("Failed to fetch messages");

      const data = await res.json();
      setMessages((prev) => ({ ...prev, [chatId]: data }));
    } catch (error) {
      console.error("Error fetching chat messages:", error);
    }
  };

  const handleNewChat = () => {
    if (!selectedUser) return;

    const tempChatId = null;
    setCurrentChat(tempChatId);
    setMessages((prev) => ({ ...prev, [tempChatId]: [] }));
  };

  const sendMessage = async () => {
    if (!input.trim() || !selectedUser) return;

    const messagePayload = {
      user_id: selectedUser.id,
      message: input,
      thread_id: currentChat,
    };

    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(messagePayload),
      });

      if (!res.ok) throw new Error("Failed to send message");

      const data = await res.json();
      const threadId = data.thread_id;
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
          { text: data.content, sender: data.sender_type === "System" ? "System" : "User" },
        ],
      }));

      setInput("");
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  const handleModalClose = () => {
    setShowUserNameModal(false);
    fetchUsers(); // Fetch users again when modal is closed
  };

  return (
    <div className="flex h-screen w-full bg-gray-50 ml-5">
      <div className="w-1/4 bg-gray-900 text-white p-6 flex flex-col space-y-4">
        {/* Add User Button */}
        <button
          className="text-sm bg-blue-500 px-6 py-3 rounded-lg hover:bg-blue-600 transition duration-300 ease-in-out transform hover:scale-105 shadow-md focus:outline-none focus:ring-2 focus:ring-blue-400 w-full"
          onClick={() => setShowUserNameModal(true)}
        >
          + Add User
        </button>
  
        {/* User Selector Dropdown */}
        <div className="flex items-center">
          <div className="flex-1">
            <UserSelector users={users} selectedUser={selectedUser} setSelectedUser={setSelectedUser} />
          </div>
        </div>
  
        {/* New Chat Button */}
        <button
          className="text-sm bg-green-500 px-6 py-3 rounded-lg hover:bg-green-600 transition duration-300 ease-in-out transform hover:scale-105 w-full"
          onClick={handleNewChat}
        >
          + New Chat
        </button>
  
        {/* Chat List */}
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
        {/* Message List */}
        <MessageList messages={messages} currentChat={currentChat} />
  
        {/* Input and Send Button */}
        <div className="flex mt-4 p-3 border bg-white rounded-lg shadow-md">
          <input
            className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
          />
          <button
            className="ml-3 p-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition duration-300 ease-in-out transform hover:scale-105"
            onClick={sendMessage}
          >
            Send
          </button>
        </div>
      </div>
  
      {/* User Name Modal */}
      {showUserNameModal && (
        <UserNamePrompt
          setSelectedUser={setSelectedUser}
          setShowUserNameModal={handleModalClose}
        />
      )}
    </div>
  );
}