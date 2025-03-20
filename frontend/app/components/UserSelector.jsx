"use client";

export default function UserSelector({ users, selectedUser, setSelectedUser }) {
  // Check if users is an array and has items
  const hasUsers = Array.isArray(users) && users.length > 0;

  return (
    <div className="w-full max-w-full overflow-x-auto">
      <select
        className="p-2 rounded-md text-black bg-white w-full max-w-full overflow-hidden text-ellipsis"
        value={selectedUser ? selectedUser.id : ""}
        onChange={(e) => {
          const userId = parseInt(e.target.value, 10);
          const newUser = hasUsers ? users.find((user) => user.id === userId) : null;
          setSelectedUser(newUser);
          localStorage.setItem("selectedUser", JSON.stringify(newUser));
        }}
      >
        <option value="" disabled>
          {hasUsers ? "Select User" : "No users available"}
        </option>
        {hasUsers &&
          users.map((user) => (
            <option
              key={user.id}
              value={user.id}
              className="text-ellipsis overflow-hidden whitespace-nowrap"
            >
              {user.name}
            </option>
          ))}
      </select>
    </div>
  );
}