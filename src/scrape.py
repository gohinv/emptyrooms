import scrape_utils
import pandas as pd
import xml.etree.ElementTree as ET

def main():
    url = "https://courses.illinois.edu/cisapp/explorer/schedule/2025/spring.xml"
    root = scrape_utils.get_root(url)
    # print(root[2][0].attrib['href'])
    # print(len(root[2]))
    num_subj = len(root[2])
    subj_urls = [root[2][i].attrib['href'] for i in range(num_subj)]
    full_data = []
    for subj_url in subj_urls:
        subj_data = scrape_utils.populate_subj(subj_url)
        full_data.extend(subj_data)

    full_df = pd.DataFrame(full_data, columns=['subject', 'course_num', 'days', 'start', 'end', 'building', 'room_number'])
    print(full_df)
    
    full_df.to_csv('all_sections.csv', index=False)


if __name__ == "__main__":
    main()
    
