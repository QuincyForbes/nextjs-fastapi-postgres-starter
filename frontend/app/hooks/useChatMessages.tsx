import { useState } from "react";
import { Message } from "../types/Message";
import { BASE_URL } from "../api/config";

type ChatMessages = Record<string, Message[]>;

export function useChatMessages() {
  const [messages, setMessages] = useState<ChatMessages>({});

  const fetchChatMessages = async (chatId: string | null) => {
    if (!chatId) return;

    try {
      const res = await fetch(`${BASE_URL}/messages?thread_id=${chatId}`);
      if (!res.ok) throw new Error("Failed to fetch messages");

      const data: Message[] = await res.json();
      setMessages((prev) => ({ ...prev, [chatId]: data }));
    } catch (error) {
      console.error("Error fetching chat messages:", error);
    }
  };

  return {
    messages,
    setMessages,
    fetchChatMessages,
  };
}
