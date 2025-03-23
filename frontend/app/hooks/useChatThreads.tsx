import { useState, useEffect } from "react";
import { BASE_URL } from "../api/config";
import { User } from "../types/User";

export function useChatThreads(selectedUser: User | null) {
  const [chats, setChats] = useState<string[]>([]);
  const [chatNames, setChatNames] = useState<Record<string, string>>({});

  useEffect(() => {
    if (!selectedUser) return;

    setChats([]);
    setChatNames({});

    fetch(`${BASE_URL}/threads?user_id=${selectedUser.id}`)
      .then((res) => (res.ok ? res.json() : []))
      .then((data: { id: string }[]) => {
        const threadIds = Array.isArray(data)
          ? data.map((thread) => thread.id)
          : [];
        setChats(threadIds.reverse());
        setChatNames(
          Object.fromEntries(threadIds.map((id) => [id, `Chat ${id}`]))
        );
      })
      .catch(() => setChats([]));
  }, [selectedUser]);

  return { chats, chatNames, setChats, setChatNames };
}
