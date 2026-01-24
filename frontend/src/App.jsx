import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";

export default function VanishingTicTacToe() {
  const [mode, setMode] = useState(null);
  const [difficulty, setDifficulty] = useState(null);
  const [board, setBoard] = useState(Array(9).fill(null));
  const [turn, setTurn] = useState("X");
  const [winner, setWinner] = useState(null);
  const [moveHistory, setMoveHistory] = useState([]);

  const handleCellClick = async (idx) => {
    if (winner || board[idx]) return; // ignore if game over or cell filled

    // 1️⃣ Update board with player's move
    const newBoard = [...board];
    newBoard[idx] = turn;

    // 2️⃣ Update moveHistory with player's move
    const playerMove = { player: turn, index: idx };
    const updatedHistory = [...moveHistory, playerMove];

    setBoard(newBoard);
    setMoveHistory(updatedHistory);

    // 3️⃣ Two Player mode
    if (mode === "two") {
      setTurn(turn === "X" ? "O" : "X");
      return;
    }

    // 4️⃣ Single Player mode: send board + history to backend for AI
    if (mode === "single" && turn === "X") {
      setTurn("O"); // AI's turn

      try {
        const response = await fetch("http://localhost:5000/move", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            board: newBoard.map((c) => c ?? " "),
            history: updatedHistory,
            player: "O",
            depth:
              difficulty === "easy"
                ? 2
                : difficulty === "medium"
                ? 4
                : difficulty === "hard"
                ? 6
                : 8,
          }),
        });

        const data = await response.json();

        if (data.move !== null && data.move !== undefined) {
          // 5️⃣ Update board with AI move
          const aiBoard = [...newBoard];
          aiBoard[data.move] = "O";
          setBoard(aiBoard);

          // 6️⃣ Update history with AI move
          setMoveHistory([...updatedHistory, { player: "O", index: data.move }]);

          // 7️⃣ Update winner if backend says game over
          if (data.winner) {
            setWinner(data.winner);
            alert(`${data.winner} wins!`);
          }
        }

        setTurn("X"); // back to player

      } catch (err) {
        console.error("AI move failed", err);
        setTurn("X"); // ensure player can still move
      }
    }
  };

  const resetGame = () => {
    setBoard(Array(9).fill(null));
    setTurn("X"); // fixed reset error
    setWinner(null);
    setMoveHistory([]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-black text-white flex flex-col">
      {/* Header */}
      <header className="flex justify-between items-center p-6">
        <h1 className="text-2xl font-bold">
          Welcome to Vanishing Tic Tac Toe Puzzle
        </h1>
        <div className="text-sm text-gray-300">
          Guest · <span className="underline cursor-pointer">Login for Saving</span>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center">
        <Card className="bg-white/10 backdrop-blur-xl border-white/20 rounded-2xl shadow-xl w-full max-w-xl">
          <CardContent className="p-8">
            {/* Mode Selection */}
            {!mode && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <h2 className="text-xl font-semibold mb-6 text-center">Let's Play</h2>
                <div className="grid grid-cols-2 gap-4">
                  <Button className="text-lg" onClick={() => setMode("single")}>
                    Single Player
                  </Button>
                  <Button className="text-lg" onClick={() => setMode("two")}>
                    Two Player
                  </Button>
                </div>
              </motion.div>
            )}

            {/* Difficulty Selection */}
            {mode === "single" && !difficulty && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <h2 className="text-xl font-semibold mb-6 text-center">Choose Difficulty</h2>
                <div className="grid grid-cols-2 gap-4">
                  {["Easy", "Medium", "Hard", "Extreme"].map((lvl) => (
                    <Button key={lvl} onClick={() => setDifficulty(lvl.toLowerCase())}>
                      {lvl}
                    </Button>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Game Board */}
            {(mode === "two" || difficulty) && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <h2 className="text-lg font-medium text-center mb-4">
                  {mode === "single" ? `Single Player · ${difficulty}` : "Two Player"}
                </h2>

                <div className="grid grid-cols-3 gap-3 w-64 mx-auto">
                  {board.map((cell, idx) => (
                    <div
                      key={idx}
                      onClick={() => handleCellClick(idx)}
                      className="h-20 w-20 flex items-center justify-center text-3xl font-bold bg-white/20 rounded-xl cursor-pointer hover:bg-white/30 transition"
                    >
                      {cell}
                    </div>
                  ))}
                </div>

                <div className="mt-6 flex justify-center gap-4">
                  <Button variant="secondary" onClick={resetGame}>
                    Reset
                  </Button>
                  <Button
                    variant="ghost"
                    onClick={() => {
                      setMode(null);
                      setDifficulty(null);
                      resetGame();
                    }}
                  >
                    Back
                  </Button>
                </div>
              </motion.div>
            )}
          </CardContent>
        </Card>
      </main>

      {/* Footer */}
      <footer className="text-center text-xs text-gray-400 p-4">
        © 2026 Vanishing Tic Tac Toe · Puzzle Mode
      </footer>
    </div>
  );
}
