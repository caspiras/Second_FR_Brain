# Project Specification

## Overview
A journaling system that tracks daily accomplishments and todos, organized by fiscal quarters and displayed via Hugo static site on localhost.

## Core Features

### 1. Todo List & Accomplishment Tracking (Integrated)
- Users can add todos in Air Force EPR format
- When a todo is marked complete, it automatically becomes an accomplishment
- Accomplishments are tracked with completion date

#### Air Force EPR Format Requirements
All todos/accomplishments must follow Air Force EPR (Enlisted Performance Report) bullet format:
- **Maximum 20 words**
- **No semicolons (;)**
- **No colons (:)**
- **No dashes (-)**
- Should start with strong action verb (Led, Managed, Developed, Coordinated, etc.)
- Be concise and impactful
- Focus on accomplishments, not tasks

Example: "Led team of 5 engineers to complete critical infrastructure upgrade ahead of schedule"

### 2. Daily Tracking
- Accomplishments are logged daily
- Each day can have multiple accomplishments

### 3. Quarterly Organization
Accomplishments are organized by fiscal quarters:
- **Q1**: January 1 - March 31
- **Q2**: April 1 - June 30
- **Q3**: July 1 - September 30
- **Q4**: October 1 - December 31

### 4. Hugo Static Site Display
- Leverages Hugo server running on local machine
- Quarterly views showing all accomplishments per quarter
- Daily views showing accomplishments by date

### 5. Daily Greeting
- Users can start their day with a greeting command
- Shows time-appropriate greeting (Good morning/afternoon/evening)
- Displays random quote from "Meditations" by Marcus Aurelius
- Shows all pending todos
- Provides motivation to complete tasks
- Available via multiple aliases: morning, hello, hi, greet
- Quote is randomly selected from **1,700+ passages** extracted from the full text of Meditations
- Quotes sourced from Project Gutenberg's public domain edition

### 6. Date/Time Awareness
- System accurately tracks completion dates for all accomplishments
- Supports viewing accomplishments by:
  - Today
  - Yesterday
  - Last 7 days (week)
  - Specific quarter
- Handles edge cases where users forget to close out their day
- All dates stored in ISO format (YYYY-MM-DD) for consistency
- Quarter assignment based on completion date, not creation date

## Data Model
- **Todo**: id, description, created_date, completed_date (null if incomplete), status
- **Accomplishment**: Completed todo with completion_date
- Accomplishments are automatically categorized by quarter based on completion_date

