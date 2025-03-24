export interface ChatListProps {
  chats: number[];
  chatNames: Record<string, string>;
  currentChat: number | null;
  setCurrentChat: (chat: number) => void;
  fetchChatMessages: (chat: number) => void;
  messages: Record<string, any>;
}
