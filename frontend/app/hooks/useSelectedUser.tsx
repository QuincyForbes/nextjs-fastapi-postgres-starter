import { useState, useEffect } from "react";
import { User } from "../types/User";

export function useSelectedUser() {
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Load from localStorage on mount
  useEffect(() => {
    try {
      const saved = localStorage.getItem("selectedUser");
      if (saved) {
        setSelectedUser(JSON.parse(saved));
      }
    } catch (e) {
      console.error("Failed to load selected user:", e);
    } finally {
      setLoading(false); 
    }
  }, []);

  // Save to localStorage on change
  useEffect(() => {
    if (selectedUser) {
      try {
        localStorage.setItem("selectedUser", JSON.stringify(selectedUser));
      } catch (e) {
        console.error("Failed to save selected user:", e);
      }
    }
  }, [selectedUser]);

  return { selectedUser, setSelectedUser, loading };
}
