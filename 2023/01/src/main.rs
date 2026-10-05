use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::Path;
use std::collections::HashMap;

fn part1() -> io::Result<()> {
    let path = Path::new("input.txt");
    let display = path.display();

    let file = match File::open(&path) {
        Err(why) => panic!("couldn't open {}: {}", display, why),
        Ok(file) => file,
    };

    let reader = io::BufReader::new(file);

    let lines: Result<Vec<_>, _> = reader.lines().collect();
    let lines = lines.unwrap_or_else(|why| panic!("couldn't read {}: {}", display, why));
    let lines: Vec<_> = lines
        .into_iter()
        .map(|line| {
            let first_num = line.chars().filter(|c| c.is_numeric()).next();
            let last_num = line.chars().filter(|c| c.is_numeric()).last();
            let combined_num = format!("{}{}", first_num.unwrap_or('0'), last_num.unwrap_or('0'));
            let combined_num = combined_num.parse::<i32>().unwrap_or(0);
            combined_num
        })
        .collect();
    let sum: i32 = lines.iter().sum();
    println!("{:?}", sum);
    Ok(())
}

fn find_and_replace_number(line: &str, num_dict: &HashMap<&str, &str>) -> String {
    let mut new_line = String::new();
    let mut temp_line = String::from(line);
    let mut skip_count = 0;

    for (i, c) in line.char_indices() {
        if skip_count > 0 {
            skip_count -= 1;
            continue;
        }

        let mut replaced = false;
        for (word, num) in num_dict {
            if temp_line.starts_with(word) {
                new_line.push_str(num);
                skip_count = word.len() - 1;
                temp_line = temp_line[word.len()..].to_string();
                replaced = true;
                break;
            }
        }

        if !replaced {
            new_line.push(c);
            temp_line = temp_line[c.len_utf8()..].to_string();
        }
    }

    new_line
}


fn part2() -> io::Result<()> {
    let path = "input.txt";
    let file = File::open(path)?;
    let reader = BufReader::new(file);

    let num_dict: HashMap<&str, &str> = [
        ("zero", "0"), ("one", "1"), ("two", "2"), ("three", "3"),
        ("four", "4"), ("five", "5"), ("six", "6"), ("seven", "7"),
        ("eight", "8"), ("nine", "9")
    ].iter().cloned().collect();

    let total_sum: i32 = reader.lines()
        .filter_map(Result::ok)
        .map(|line| line.to_lowercase())
        .map(|line| find_and_replace_number(&line, &num_dict))
        .filter_map(|line| {
            let nums: Vec<_> = line.chars().filter(|c| c.is_digit(10)).collect();
            nums.first().and_then(|&first_num| nums.last().map(|&last_num| [first_num, last_num].iter().collect::<String>()))
        })
        .filter_map(|combined_num| combined_num.parse::<i32>().ok())
        .sum();

    println!("{}", total_sum);

    Ok(())
}
fn main() -> io::Result<()> {
    part1()?;
    part2()?;
    Ok(())
}
