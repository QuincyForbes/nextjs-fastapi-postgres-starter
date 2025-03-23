import { useState, useEffect } from "react";
import { User } from "../types/User";
import { BASE_URL } from "../api/config";

export function useUsers() {
  const [users, setUsers] = useState<User[] | null>(null);

  useEffect(() => {
    fetch(`${BASE_URL}/users`)
      .then((res) => res.json())
      .then((data: User[]) => {
        setUsers(data?.length === 0 ? [] : data);
      })
      .catch(() => setUsers([]));
  }, []);

  return { users, refreshUsers: () => {
    fetch(`${BASE_URL}/users`)
      .then((res) => res.json())
      .then((data: User[]) => {
        setUsers(data?.length === 0 ? [] : data);
      })
      .catch(() => setUsers([]));
  }, setUsers };
}
