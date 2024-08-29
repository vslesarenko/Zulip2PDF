
def extract_lines(filename, target_words, stop_symbol):
    channel_list=[]
    with open(filename, 'r') as file:
        for line in file:
            for word in target_words:
                if word in line:
                    start_index = line.index(word)
                    end_index = line.find(stop_symbol, start_index)
                    if end_index == -1:
                        end_index = len(line)
                    new_channel=line[start_index:end_index].strip()[8:]
                    print(new_channel)
                    channel_list.append(new_channel)
    return channel_list


# Example usage:
filename = 'html_raw.txt'
filename_out='channel_list.txt'
target_words = ['#narrow']  # Replace with your specific words
stop_symbol = '"'  # Replace with your specific stop symbol
extracted_lines=extract_lines(filename, target_words, stop_symbol)

with open(filename_out, 'w') as file:
    for line in extracted_lines:
        file.write(line + '\n')