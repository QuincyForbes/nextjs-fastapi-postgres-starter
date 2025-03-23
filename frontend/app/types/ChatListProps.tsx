export interface ChatListProps {
  chats: string[];
  chatNames: Record<string, string>;
  currentChat: string | null;
  setCurrentChat: (chat: string) => void;
  fetchChatMessages: (chat: string) => void;
  messages: Record<string, any>;
}
