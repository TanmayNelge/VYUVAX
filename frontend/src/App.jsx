import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";

export default function VanishingTicTacToe() {
  const [mode, setMode] = useState(null); // null | 'single' | 'two'
  const [difficulty, setDifficulty] = useState(null); // easy | medium | hard | extreme
  const [board, setBoard] = useState(Array(9).fill(null));
  const [turn, setTurn] = useState("X");

  const handleCellClick = (idx) => {
    if (board[idx]) return;
    const newBoard = [...board];
    newBoard[idx] = turn;
    setBoard(newBoard);
    setTurn(turn === "X" ? "O" : "X");
  };

  const resetGame = () => {
    setBoard(Array(9).fill(null));
    setTurn("X");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-black text-white flex flex-col">
      {/* Header */}
      <header className="flex justify-between items-center p-6">
        <h1 className="text-2xl font-bold">Welcome to Vanishing Tic Tac Toe Puzzle</h1>
        <div className="text-sm text-gray-300">
          Guest · <span className="underline cursor-pointer">Login for Saving</span>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center">
        <Card className="bg-white/10 backdrop-blur-xl border-white/20 rounded-2xl shadow-xl w-full max-w-xl">
          <CardContent className="p-8">
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
