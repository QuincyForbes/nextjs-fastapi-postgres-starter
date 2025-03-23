import { User } from "./User";

export interface UserNamePromptProps {
  setSelectedUser: (user: User) => void;
  setShowUserNameModal: (show: boolean) => void;
}
