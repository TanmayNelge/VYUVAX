// import { useState } from "react";
// import { Card, CardContent } from "@/components/ui/card";
// import { Button } from "@/components/ui/button";
// import { motion } from "framer-motion";

// export default function VanishingTicTacToe() {
//   const [mode, setMode] = useState(null);
//   const [difficulty, setDifficulty] = useState(null);
//   const [board, setBoard] = useState(Array(9).fill(null));
//   const [turn, setTurn] = useState("X");
//   const [winner, setWinner] = useState(null);
//   const [moveHistory, setMoveHistory] = useState([]);

//   const handleCellClick = async (idx) => {
//     if (winner || board[idx]) return; 


//     const newBoard = [...board];
//     newBoard[idx] = turn;

//     const playerMove = { player: turn, index: idx };
//     const updatedHistory = [...moveHistory, playerMove];

//     setBoard(newBoard);
//     setMoveHistory(updatedHistory);

//     if (mode === "two") {
//       setTurn(turn === "X" ? "O" : "X");
//       return;
//     }

//   //   if (mode === "single" && turn === "X") {
//   //     setTurn("O");

//   //     try {
//   //       const response = await fetch("http://localhost:5000/move", {
//   //         method: "POST",
//   //         headers: { "Content-Type": "application/json" },
//   //         body: JSON.stringify({
//   //           board: newBoard.map((c) => c ?? " "),
//   //           history: updatedHistory,
//   //           player: "O",
//   //           depth:
//   //             difficulty === "easy"
//   //               ? 2
//   //               : difficulty === "medium"
//   //               ? 4
//   //               : difficulty === "hard"
//   //               ? 6
//   //               : 8,
//   //         }),
//   //       });

//   //       const data = await response.json();

//   //       if (data.move !== null && data.move !== undefined) {
//   //         const aiBoard = [...newBoard];
//   //         aiBoard[data.move] = "O";
//   //         setBoard(aiBoard);


//   //         setMoveHistory([...updatedHistory, { player: "O", index: data.move }]);

//   //         if (data.winner) {
//   //           setWinner(data.winner);
//   //           alert(`${data.winner} wins!`);
//   //         }
//   //       }

//   //       setTurn("X"); 

//   //     } catch (err) {
//   //       console.error("AI move failed", err);
//   //       setTurn("X"); 
//   //     }
//   //   }
//   // };
//   if (mode === "single" && turn === "X") {
//   setTurn("O"); // AI's turn

//   try {
//     const response = await fetch("http://localhost:5000/move", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({
//         board: newBoard.map((c) => c ?? " "),
//         history: updatedHistory,
//         player: "O",
//         depth:
//           difficulty === "easy"
//             ? 2
//             : difficulty === "medium"
//             ? 4
//             : difficulty === "hard"
//             ? 6
//             : 8,
//       }),
//     });

//     if (!response.ok) {
//       console.error("Backend error:", response.status, response.statusText);
//       setTurn("X");
//       return;
//     }

//     const data = await response.json();

//     if (data.move === null || data.move === undefined) {
//       console.warn("No move returned from AI", data);
//       setTurn("X");
//       return;
//     }

//     const aiBoard = [...newBoard];
//     aiBoard[data.move] = "O";
//     setBoard(aiBoard);

//     setMoveHistory([...updatedHistory, { player: "O", index: data.move }]);

//     if (data.winner) {
//       setWinner(data.winner);
//       alert(`${data.winner} wins!`);
//     }

//     setTurn("X"); 

//   } catch (err) {

//     console.error("AI move failed:", err);
//     setTurn("X"); 
//   }
// }
//   };


//   const resetGame = () => {
//     setBoard(Array(9).fill(null));
//     setTurn("X"); 
//     setWinner(null);
//     setMoveHistory([]);
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-black text-white flex flex-col">
//       {/* Header */}
//       <header className="flex justify-between items-center p-6">
//         <h1 className="text-2xl font-bold">
//           Welcome to Vanishing Tic Tac Toe Puzzle
//         </h1>
//         <div className="text-sm text-gray-300">
//           Guest · <span className="underline cursor-pointer">Login for Saving</span>
//         </div>
//       </header>

//       {/* Main Content */}
//       <main className="flex-1 flex items-center justify-center">
//         <Card className="bg-white/10 backdrop-blur-xl border-white/20 rounded-2xl shadow-xl w-full max-w-xl">
//           <CardContent className="p-8">
//             {/* Mode Selection */}
//             {!mode && (
//               <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
//                 <h2 className="text-xl font-semibold mb-6 text-center">Let's Play</h2>
//                 <div className="grid grid-cols-2 gap-4">
//                   <Button className="text-lg" onClick={() => setMode("single")}>
//                     Single Player
//                   </Button>
//                   <Button className="text-lg" onClick={() => setMode("two")}>
//                     Two Player
//                   </Button>
//                 </div>
//               </motion.div>
//             )}

//             {/* Difficulty Selection */}
//             {mode === "single" && !difficulty && (
//               <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
//                 <h2 className="text-xl font-semibold mb-6 text-center">Choose Difficulty</h2>
//                 <div className="grid grid-cols-2 gap-4">
//                   {["Easy", "Medium", "Hard", "Extreme"].map((lvl) => (
//                     <Button key={lvl} onClick={() => setDifficulty(lvl.toLowerCase())}>
//                       {lvl}
//                     </Button>
//                   ))}
//                 </div>
//               </motion.div>
//             )}

//             {/* Game Board */}
//             {(mode === "two" || difficulty) && (
//               <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
//                 <h2 className="text-lg font-medium text-center mb-4">
//                   {mode === "single" ? `Single Player · ${difficulty}` : "Two Player"}
//                 </h2>

//                 <div className="grid grid-cols-3 gap-3 w-64 mx-auto">
//                   {board.map((cell, idx) => (
//                     <div
//                       key={idx}
//                       onClick={() => handleCellClick(idx)}
//                       className="h-20 w-20 flex items-center justify-center text-3xl font-bold bg-white/20 rounded-xl cursor-pointer hover:bg-white/30 transition"
//                     >
//                       {cell}
//                     </div>
//                   ))}
//                 </div>

//                 <div className="mt-6 flex justify-center gap-4">
//                   <Button variant="secondary" onClick={resetGame}>
//                     Reset
//                   </Button>
//                   <Button
//                     variant="ghost"
//                     onClick={() => {
//                       setMode(null);
//                       setDifficulty(null);
//                       resetGame();
//                     }}
//                   >
//                     Back
//                   </Button>
//                 </div>
//               </motion.div>
//             )}
//           </CardContent>
//         </Card>
//       </main>

//       {/* Footer */}
//       <footer className="text-center text-xs text-gray-400 p-4">
//         © 2026 Vanishing Tic Tac Toe · Puzzle Mode
//       </footer>
//     </div>
//   );
// }


import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";

export default function VanishingTicTacToe() {
  const [mode, setMode] = useState(null);
  const [difficulty, setDifficulty] = useState(null);
  const [board, setBoard] = useState(Array(9).fill(" "));
  const [history, setHistory] = useState([]);
  const [turn, setTurn] = useState("X");
  const [winner, setWinner] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const depthMap = {
    easy: 2,
    medium: 4,
    hard: 6,
    extreme: 8,
  };

  const handleCellClick = async (idx) => {
    if (board[idx] !== " " || winner || isLoading) return;

    // ---- TWO PLAYER MODE (NO BACKEND AI) ----
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

    // ---- SINGLE PLAYER MODE (BACKEND CONTROLS AI) ----
    try {
      setIsLoading(true);
      const moveDepth = depthMap[difficulty] || 4; 
      console.log(`Requesting move with depth: ${moveDepth} (difficulty: ${difficulty})`);

      const res = await fetch("http://localhost:8000/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          board,
          history,
          player: "X",
          move_index: idx,
          depth: moveDepth,
          mode: "single",
        }),
      });

      const data = await res.json();
      if (data.board) {
        setBoard(data.board);
        setHistory(data.history);
        setWinner(data.winner);
      } else {
        console.error("Invalid data received:", data);
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
    setTurn("X");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-black text-white flex flex-col">
      <header className="p-6 text-center text-xl font-bold">
        Vanishing Tic Tac Toe
      </header>

      <main className="flex-1 flex items-center justify-center">
        <Card className="bg-white/10 border-white/20 w-full max-w-xl">
          <CardContent className="p-8">

            {!mode && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <h2 className="text-center mb-6">Choose Mode</h2>
                <div className="grid grid-cols-2 gap-4">
                  <Button onClick={() => setMode("single")}>Single Player</Button>
                  <Button onClick={() => setMode("two")}>Two Player</Button>
                </div>
              </motion.div>
            )}

            {mode === "single" && !difficulty && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <h2 className="text-center mb-6">Choose Difficulty</h2>
                <div className="grid grid-cols-2 gap-4">
                  {["easy", "medium", "hard", "extreme"].map((lvl) => (
                    <Button key={lvl} onClick={() => setDifficulty(lvl)}>
                      {lvl.toUpperCase()}
                    </Button>
                  ))}
                </div>
              </motion.div>
            )}

            {(mode === "two" || difficulty) && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <h2 className="text-center mb-4">
                  {winner ? `${winner} wins!` : `Turn: ${turn}`}
                </h2>

                <div className="grid grid-cols-3 gap-3 w-64 mx-auto">
                  {board.map((cell, idx) => {
                    const playerMoves = history.filter((m) => m.player === turn);
                    const opponentMoves = history.filter((m) => m.player !== turn);

                    const isPlayerVanishing =
                      playerMoves.length >= 3 && playerMoves[0].index === idx && !winner;
                    const isOpponentVanishing =
                      opponentMoves.length >= 3 && opponentMoves[0].index === idx && !winner;

                    let bgClass = "bg-white/20";
                    if (isPlayerVanishing) bgClass = "bg-red-500/50";
                    else if (isOpponentVanishing) bgClass = "bg-green-500/50";

                    return (
                      <div
                        key={idx}
                        onClick={() => handleCellClick(idx)}
                        className={`h-20 w-20 flex items-center justify-center text-3xl font-bold rounded-xl cursor-pointer hover:bg-white/30 transition-all ${bgClass}`}
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

