import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";

export default function VanishingTicTacToe() {
  const [mode, setMode] = useState(null);
  const [playerSymbol, setPlayerSymbol] = useState(null); // Tracks if user is X or O
  const [difficulty, setDifficulty] = useState(null);
  const [board, setBoard] = useState(Array(9).fill(" "));
  const [history, setHistory] = useState([]);
  const [turn, setTurn] = useState("X"); // X always goes first
  const [winner, setWinner] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const depthMap = {
    easy: 2,
    medium: 4,
    hard: 6,
    extreme: 8,
  };

  // --- THE "O" EDGE CASE ---
  // If the user chooses 'O', X still goes first. This triggers the AI to make the opening move.
  useEffect(() => {
    if (
      mode === "single" &&
      playerSymbol === "O" &&
      difficulty &&
      board.every((c) => c === " ") &&
      !winner &&
      !isLoading
    ) {
      triggerFirstAIMove();
    }
  }, [mode, playerSymbol, difficulty]);

  const triggerFirstAIMove = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("http://localhost:8000/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          board: Array(9).fill(" "),
          history: [],
          player: "O", // Tell backend the human is 'O'
          move_index: null, // No human move yet, just let AI calculate
          depth: depthMap[difficulty],
          mode: "single",
        }),
      });
      const data = await res.json();
      if (data.board) {
        setBoard(data.board);
        setHistory(data.history);
        setWinner(data.winner);
        setTurn("O"); // Now it's the user's turn
      }
    } catch (err) {
      console.error("AI error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCellClick = async (idx) => {
    // Prevent clicks if cell is taken, game is over, loading, or if it's the AI's turn
    if (
      board[idx] !== " " ||
      winner ||
      isLoading ||
      (mode === "single" && turn !== playerSymbol)
    ) return;

    // ---- TWO PLAYER MODE ----
    if (mode === "two") {
      try {
        const res = await fetch("http://localhost:8000/move", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            board,
            history,
            player: turn,
            move_index: idx,
            mode: "two",
          }),
        });

        const data = await res.json();
        setBoard(data.board);
        setHistory(data.history);
        setWinner(data.winner);
        setTurn(turn === "X" ? "O" : "X");
      } catch (err) {
        console.error(err);
      }
      return;
    }

    // ---- SINGLE PLAYER MODE ----
    try {
      setIsLoading(true);
      setTurn(playerSymbol === "X" ? "O" : "X"); // Visual turn switch

      const res = await fetch("http://localhost:8000/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          board,
          history,
          player: playerSymbol, // Dynamically send the user's chosen symbol
          move_index: idx,
          depth: depthMap[difficulty],
          mode: "single",
        }),
      });

      const data = await res.json();
      if (data.board) {
        setBoard(data.board);
        setHistory(data.history);
        setWinner(data.winner);
        setTurn(playerSymbol); // Switch turn back to user
      }
    } catch (err) {
      console.error("AI error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const resetGame = () => {
    setBoard(Array(9).fill(" "));
    setHistory([]);
    setWinner(null);
    setTurn("X"); // X always starts a new round
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-black text-white flex flex-col">
      <header className="p-6 text-center text-xl font-bold">
        Vanishing Tic Tac Toe
      </header>

      <main className="flex-1 flex items-center justify-center">
        <Card className="bg-white/10 border-white/20 w-full max-w-xl">
          <CardContent className="p-8">

            {/* Step 1: Choose Mode */}
            {!mode && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <h2 className="text-center mb-6 text-xl">Choose Mode</h2>
                <div className="grid grid-cols-2 gap-4">
                  <Button onClick={() => setMode("single")}>Single Player</Button>
                  <Button onClick={() => setMode("two")}>Two Player</Button>
                </div>
              </motion.div>
            )}

            {/* Step 2: Choose Symbol (Only in Single Player) */}
            {mode === "single" && !playerSymbol && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <h2 className="text-center mb-6 text-xl">Choose Your Symbol</h2>
                <div className="grid grid-cols-2 gap-4">
                  <Button onClick={() => setPlayerSymbol("X")}>Play as X (Goes First)</Button>
                  <Button onClick={() => setPlayerSymbol("O")}>Play as O (Goes Second)</Button>
                </div>
              </motion.div>
            )}

            {/* Step 3: Choose Difficulty */}
            {mode === "single" && playerSymbol && !difficulty && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <h2 className="text-center mb-6 text-xl">Choose Difficulty</h2>
                <div className="grid grid-cols-2 gap-4">
                  {["easy", "medium", "hard", "extreme"].map((lvl) => (
                    <Button key={lvl} onClick={() => setDifficulty(lvl)}>
                      {lvl.toUpperCase()}
                    </Button>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Game Board */}
            {(mode === "two" || difficulty) && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <h2 className="text-center mb-4 text-lg">
                  {winner ? `${winner} wins!` : isLoading ? "AI is thinking..." : `Turn: ${turn}`}
                </h2>

                <div className="grid grid-cols-3 gap-3 w-64 mx-auto">
                  {board.map((cell, idx) => {
                    // Logic to highlight vanishing pieces
                    const xMoves = history.filter((m) => m.player === "X");
                    const oMoves = history.filter((m) => m.player === "O");

                    const isXVanishing = xMoves.length >= 3 && xMoves[0].index === idx && !winner;
                    const isOVanishing = oMoves.length >= 3 && oMoves[0].index === idx && !winner;

                    let bgClass = "bg-white/20";
                    if (isXVanishing) bgClass = "bg-red-500/50";
                    else if (isOVanishing) bgClass = "bg-blue-500/50";

                    return (
                      <div
                        key={idx}
                        onClick={() => handleCellClick(idx)}
                        className={`h-20 w-20 flex items-center justify-center text-4xl font-bold rounded-xl cursor-pointer hover:bg-white/30 transition-all ${bgClass}`}
                      >
                        {cell !== " " ? cell : ""}
                      </div>
                    );
                  })}
                </div>

                <div className="mt-6 flex justify-center gap-4">
                  <Button onClick={resetGame}>Reset</Button>
                  <Button
                    variant="ghost"
                    onClick={() => {
                      setMode(null);
                      setPlayerSymbol(null);
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
    </div>
  );
}
