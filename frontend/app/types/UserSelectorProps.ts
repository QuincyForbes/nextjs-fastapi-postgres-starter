import { User } from "./User";

export interface UserSelectorProps {
  users: User[];
  selectedUser: User | null;
  setSelectedUser: (user: User | null) => void;
}
