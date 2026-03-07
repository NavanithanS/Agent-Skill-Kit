/**
 * Calculates a date 30 days from now.
 * Usage: node date_calculator.js
 */

const today = new Date();
const targetDate = new Date(today);
targetDate.setDate(today.getDate() + 30);

console.log(JSON.stringify({
    today: today.toISOString().split('T')[0],
    target_date: targetDate.toISOString().split('T')[0],
    target_month: targetDate.toLocaleString('default', { month: 'long' }),
    target_day: targetDate.getDate(),
    target_year: targetDate.getFullYear()
}));
