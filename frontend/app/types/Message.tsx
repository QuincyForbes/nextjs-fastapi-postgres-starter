export interface Message {
  sender?: string;
  sender_type?: string;
  text?: string;
  content?: string;
  [key: string]: any;
}
