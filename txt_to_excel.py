import pandas as pd
def txt_to_excel(inputfile='查询结果2.txt', outfile='out2.xlsx'):
    """
    :param inputfile:
    :param outfile:
    :return:
    """
    f = open(inputfile, encoding='gb18030', errors='ignore')
    df = pd.read_csv(f, sep=',', skiprows=1, header=None)
    df.columns = ["phone", "name", "label", "endtime", "handuptime", "operate"]
    df['phone'] = df['phone'].astype("str")
    print(df.head(5))
    df.to_excel(outfile, index=False)

if __name__ == "__main__":
    # txt_to_excel(inputfile='查询结果.txt', outfile='out1.xlsx')

    import argparse
    parser = argparse.ArgumentParser(description='manual to this script txt_to_excel')
    parser.add_argument('-i', '--inputfile', help='path of input txt file ',  type=str, default=None)
    parser.add_argument('-o', '--outfile', help='path of out xlsx filee', type=str, default=None)
    args = parser.parse_args()
    print(args.inputfile, args.outfile)
    txt_to_excel(inputfile=args.inputfile, outfile=args.outfile)
    pass
