import { Message } from "./Message";

export interface MessageListProps {
  messages: Record<string, Message[]>;
  currentChat: string | null;
}
