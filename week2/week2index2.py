#Q1
def find_and_print(messages, current_station):
    min_distance = float('inf')
    closest_friend = None
    current_station_index = stations.index(current_station)
    for friend, message in messages.items():
        friend_station = extract_station(message)
        if friend_station is None:
            continue
        friend_station_index = stations.index(friend_station)
        if current_station_index == stations.index("Qizhang") and friend_station == "Xiaobitan":
            closest_friend = friend
            break
        if current_station_index == stations.index("Xindian City Hall") and friend_station == "Xiaobitan":
            continue
        distance = abs(current_station_index - friend_station_index)
        if distance < min_distance:
            min_distance = distance
            closest_friend = friend
    print(closest_friend)
def extract_station(message):
    for station in stations:
        if station in message:
            return station
    return None
stations = [
    "Songshan", "Nanjing Sanmin", "Taipei Arena", "Nanjing Fuxing", 
    "Songjiang Nanjing", "Zhongshan", "Beimen", "Ximen", "Xiaonanmen", 
    "Chiang Kai-shek Memorial Hall", "Guting", "Taipower Building", 
    "Gongguan", "Wanlong", "Jingmei", "Dapinglin", "Qizhang", 
    "Xiaobitan", "Xindian City Hall", "Xindian"
]
messages = {
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Leslie": "I'm at home near Xiaobitan station.",
    "Vivian": "I'm at Xindian station waiting for you."
}
find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian

#Q2
def book(consultants, hour, duration, criteria):
    for consultant in consultants:
        if 'schedule' not in consultant:
            consultant['schedule'] = [True]*24

    available_consultants = [consultant for consultant in consultants if all(consultant['schedule'][i] for i in range(hour, hour+duration))]

    if len(available_consultants) == 0:
        print("No Service")
        return

    if criteria == "price":
        available_consultants.sort(key=lambda x: x['price'])
    elif criteria == "rate":
        available_consultants.sort(key=lambda x: x['rate'], reverse=True)
    chosen_consultant = available_consultants[0]
    for i in range(hour, hour + duration):
        chosen_consultant['schedule'][i] = False
    print(chosen_consultant['name'])
consultants = [
    {"name":"John", "rate":4.5, "price":1000},
    {"name":"Bob", "rate":3, "price":1200},
    {"name":"Jenny", "rate":3.8, "price":800}
]
book(consultants, 15, 1, "price") # Jenny
book(consultants, 11, 2, "price") # Jenny
book(consultants, 10, 2, "price") # John
book(consultants, 20, 2, "rate") # John
book(consultants, 11, 1, "rate") # Bob
book(consultants, 11, 2, "rate") # No Service
book(consultants, 14, 3, "price") # John

#Q3
def func(*data):
    middle_names = {}
    for name in data:
        if len(name) == 2 or len(name) == 3:
            middle_name = name[1]
        elif len(name) == 4 or len(name) == 5:
            middle_name = name[2]
        else:
            continue

        if middle_name in middle_names:
            middle_names[middle_name] += 1
        else:
            middle_names[middle_name] = 1

    unique_middle_names = [middle_name for middle_name, count in middle_names.items() if count == 1]

    if len(unique_middle_names) == 0:
        print("沒有")
    else:
        for name in data:
            if (len(name) == 2 or len(name) == 3) and name[1] in unique_middle_names:
                print(name)
            elif (len(name) == 4 or len(name) == 5) and name[2] in unique_middle_names:
                print(name)
func("彭大牆", "陳王明雅", "吳明")  # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花")  # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花")  # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆")  # print 夏曼藍波安

#Q4
def getNumber(index):
    group = index // 3
    position = index % 3
    base = group * 7
    if position == 0:
        result = base
    elif position == 1:
        result = base + 4
    else:
        result = base + 4 + 4   
    print(result)
    return result
getNumber(1) # print 4
getNumber(5) # print 15
getNumber(10) # print 25
getNumber(30) # print 70

