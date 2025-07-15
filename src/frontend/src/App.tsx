// src/App.tsx - Main UI for HebRabbAI Agent 2: Interactive Reading Companion
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './index.css';

// Alias import - resolves to data\text\hebrew_bible_with_nikkud.json
import tanakhData from '@data/hebrew_bible_with_nikkud.json';

// Type-safe interfaces
interface Verse { book: string; chapter: number; verse: number; text: string; }
interface TTSResponse { audioUrl: string; timings: { word: string; start: number; end: number }[]; }
interface LexiconEntry { ipa: string; morph: string; }

const App: React.FC = () => {
  const [verses, setVerses] = useState<Verse[]>([]);
  const [selectedVerse, setSelectedVerse] = useState<Verse | null>(null);
  const [highlightedWord, setHighlightedWord] = useState<number>(-1);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1.0);
  const [lexiconPopup, setLexiconPopup] = useState<LexiconEntry | null>(null);
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    // Debug: Log if tanakhData loaded
    if (!tanakhData) {
      console.error('tanakhData is undefined - check alias/import path');
      alert('tanakhData undefined - Verify @data alias in vite.config.ts and JSON path.');
      return;
    }
    console.log('Raw Tanakh Data Type:', typeof tanakhData, 'Keys (books):', Object.keys(tanakhData).slice(0, 5));

    // Robust load with flattening (matches {book: [chapters [verses [words]]]})
    try {
      const flatVerses: Verse[] = [];
      let skippedBooks = 0;
      for (const book in tanakhData) {
        const chapters = tanakhData[book];
        if (!Array.isArray(chapters)) {
          console.warn(`Skipping non-array book ${book}`);
          skippedBooks++;
          continue;
        }
        console.log(`Book ${book} has ${chapters.length} chapters`);

        chapters.forEach((versesArr, chapterIndex) => {
          if (!Array.isArray(versesArr)) {
            console.warn(`Skipping non-array chapter in ${book} at index ${chapterIndex}`);
            return;
          }
          console.log(`  Chapter ${chapterIndex + 1} has ${versesArr.length} verses`);

          versesArr.forEach((words, verseIndex) => {
            if (!Array.isArray(words)) {
              console.warn(`Skipping non-array verse in ${book} chapter ${chapterIndex + 1} at index ${verseIndex}`);
              return;
            }
            const text = words.join(' ');  // Join words, includes "ס"/"פ"
            flatVerses.push({
              book,
              chapter: chapterIndex + 1,
              verse: verseIndex + 1,
              text
            });
          });
        });
      }
      if (skippedBooks > 0) console.warn(`Skipped ${skippedBooks} books due to structure issues`);
      if (flatVerses.length === 0) throw new Error('Empty data after flattening - check console for skipped items/structure');
      console.log('Flattened Verses Sample:', flatVerses.slice(0, 5));
      setVerses(flatVerses.slice(0, 1000));  // Limit for dev scalability (full in prod)
    } catch (err) {
      console.error('Tanakh load/flatten error:', err);
      alert('Failed to load/flatten Tanakh from data\\text. Check console (F12) for skipped/structure logs and report.');
      setVerses([]);
    }

    // Offline stub
    const storedVerse = localStorage.getItem('selectedVerse');
    if (storedVerse) setSelectedVerse(JSON.parse(storedVerse));
  }, []);

  // ... rest of code unchanged (handleVerseSelect, handlePlay, etc. from prior full code)

  return (
    <div className="container mx-auto p-4 dir-rtl">
      <h1 className="text-2xl font-bold mb-4 sm:text-3xl">HebRabbAI - Interactive Reading Companion</h1>
      <select onChange={e => handleVerseSelect(verses[parseInt(e.target.value)])} className="mb-4 p-2 border w-full sm:w-auto" aria-label="Select Verse" role="combobox">
        <option>Select Verse</option>
        {verses.map((v, i) => <option key={i} value={i}>{`${v.book} ${v.chapter}:${v.verse}`}</option>)}
      </select>
      {selectedVerse && (
        <p className="text-lg mb-4 sm:text-xl md:text-2xl">
          {selectedVerse.text.split(' ').map((word, i) => (
            <span key={i} onClick={() => handleWordClick(word)} className={`cursor-pointer ${i === highlightedWord ? 'bg-yellow-300' : ''}`} aria-label={`Word: ${word}, click for lexicon`} role="button" tabIndex={0}>
              {word}{' '}
            </span>
          ))}
        </p>
      )}
      <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4 mb-4">
        <button onClick={isPlaying ? handlePause : handlePlay} className="bg-blue-500 text-white p-2 rounded" aria-pressed={isPlaying} aria-label={isPlaying ? 'Pause' : 'Play'}>
          {isPlaying ? 'Pause' : 'Play'}
        </button>
        <label className="flex items-center">
          Speed: <input type="range" min="0.5" max="2.0" step="0.1" value={speed} onChange={e => setSpeed(parseFloat(e.target.value))} className="ml-2 w-full sm:w-32" aria-label="Speed" />
        </label>
      </div>
      <audio ref={audioRef} onEnded={() => setIsPlaying(false)} />
      {lexiconPopup && (
        <div className="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center" role="dialog" aria-modal="true">
          <div className="bg-white p-4 rounded max-w-md">
            <h2 className="text-xl font-bold">Word Analysis</h2>
            <p>IPA: {lexiconPopup.ipa}</p>
            <p>Morph: {lexiconPopup.morph}</p>
            <button onClick={() => setLexiconPopup(null)} className="bg-red-500 text-white p-2 mt-2" aria-label="Close">
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;