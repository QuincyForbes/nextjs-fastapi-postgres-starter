import { Message } from "./Message";

export interface MessageListProps {
  messages: Record<number, Message[]>;
  currentChat: number | null;
}
