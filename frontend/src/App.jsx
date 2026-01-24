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

const WIN_LINES = [
  [0,1,2],[3,4,5],[6,7,8],
  [0,3,6],[1,4,7],[2,5,8],
  [0,4,8],[2,4,6],
];

function checkWinner(board) {
  for (const [a,b,c] of WIN_LINES) {
    if (board[a] !== " " && board[a] === board[b] && board[a] === board[c]) {
      return board[a];
    }
  }
  return null;
}

function applyVanishing(board, history, player) {
  const playerMoves = history.filter(m => m.player === player);
  if (playerMoves.length > 3) {
    const removed = playerMoves[0];
    board[removed.index] = " ";
    history = history.filter(m => m !== removed);
  }
  return { board, history };
}

export default function VanishingTicTacToe() {
  const [mode, setMode] = useState(null);
  const [difficulty, setDifficulty] = useState(null);
  const [board, setBoard] = useState(Array(9).fill(" "));
  const [turn, setTurn] = useState("X");
  const [winner, setWinner] = useState(null);
  const [history, setHistory] = useState([]);

  const handleCellClick = async (idx) => {
    if (winner || board[idx] !== " ") return;

    let newBoard = [...board];
    let newHistory = [...history, { player: turn, index: idx }];
    newBoard[idx] = turn;

    ({ board: newBoard, history: newHistory } =
      applyVanishing(newBoard, newHistory, turn));

    const win = checkWinner(newBoard);
    setBoard(newBoard);
    setHistory(newHistory);

    if (win) {
      setWinner(win);
      return;
    }

    if (mode === "two") {
      setTurn(turn === "X" ? "O" : "X");
      return;
    }

    setTurn("O");

    try {
      const response = await fetch("http://localhost:5000/move", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          board: newBoard,
          history: newHistory,
          player: "O",
          depth:
            difficulty === "easy" ? 2 :
            difficulty === "medium" ? 4 :
            difficulty === "hard" ? 6 : 8,
        }),
      });

      const data = await response.json();
      if (data.move === null || data.move === undefined) {
        setTurn("X");
        return;
      }

      let aiBoard = [...newBoard];
      let aiHistory = [...newHistory, { player: "O", index: data.move }];
      aiBoard[data.move] = "O";

      ({ board: aiBoard, history: aiHistory } =
        applyVanishing(aiBoard, aiHistory, "O"));

      const aiWin = checkWinner(aiBoard);
      setBoard(aiBoard);
      setHistory(aiHistory);

      if (aiWin) {
        setWinner(aiWin);
        return;
      }

      setTurn("X");

    } catch (err) {
      console.error("AI error:", err);
      setTurn("X");
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
              <motion.div initial={{opacity:0}} animate={{opacity:1}}>
                <h2 className="text-center mb-6">Choose Mode</h2>
                <div className="grid grid-cols-2 gap-4">
                  <Button onClick={() => setMode("single")}>Single Player</Button>
                  <Button onClick={() => setMode("two")}>Two Player</Button>
                </div>
              </motion.div>
            )}

            {mode === "single" && !difficulty && (
              <motion.div initial={{opacity:0}} animate={{opacity:1}}>
                <h2 className="text-center mb-6">Difficulty</h2>
                <div className="grid grid-cols-2 gap-4">
                  {["easy","medium","hard","extreme"].map(lvl => (
                    <Button key={lvl} onClick={() => setDifficulty(lvl)}>
                      {lvl.toUpperCase()}
                    </Button>
                  ))}
                </div>
              </motion.div>
            )}

            {(mode === "two" || difficulty) && (
              <motion.div initial={{opacity:0}} animate={{opacity:1}}>
                <h2 className="text-center mb-4">
                  {winner ? `${winner} Wins!` : `Turn: ${turn}`}
                </h2>

                <div className="grid grid-cols-3 gap-3 w-64 mx-auto">
                  {board.map((cell, i) => (
                    <div
                      key={i}
                      onClick={() => handleCellClick(i)}
                      className="h-20 w-20 flex items-center justify-center text-3xl font-bold bg-white/20 rounded-xl cursor-pointer hover:bg-white/30"
                    >
                      {cell !== " " ? cell : ""}
                    </div>
                  ))}
                </div>

                <div className="mt-6 flex justify-center gap-4">
                  <Button onClick={resetGame}>Reset</Button>
                  <Button variant="ghost" onClick={() => {
                    setMode(null);
                    setDifficulty(null);
                    resetGame();
                  }}>
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
