import { useState } from "react";

export default function UserNamePrompt({ setSelectedUser, setShowUserNameModal }) {
  const [userName, setUserName] = useState("");

  const handleSubmit = async () => {
    if (userName.trim()) {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/v1/users", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ name: userName }),
        });
  
        if (response.ok) {
          const data = await response.json();
          setSelectedUser(data);
          localStorage.setItem("selectedUser", JSON.stringify(data)); 
          setShowUserNameModal(false);
        }
      } catch (error) {
        console.error("Error creating user:", error);
      }
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      handleSubmit(); 
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div className="bg-white p-6 rounded-lg shadow-lg w-1/3">
        <h2 className="text-xl mb-4">Please enter your name</h2>
        <input
          type="text"
          className="w-full p-3 border rounded-lg"
          value={userName}
          onChange={(e) => setUserName(e.target.value)}
          onKeyDown={handleKeyDown} // Add keydown event listener
          placeholder="Enter name"
        />
        <div className="mt-4 flex justify-between">
          <button
            className="px-4 py-2 bg-gray-500 text-white rounded-md"
            onClick={() => setShowUserNameModal(false)}
          >
            Cancel
          </button>
          <button
            className="px-4 py-2 bg-green-500 text-white rounded-md"
            onClick={handleSubmit}
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
}
