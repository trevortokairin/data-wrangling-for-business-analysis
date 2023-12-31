import pandas as pd
import numpy as np


def bbanalyze(filename='baseball.csv'):
    # reads the baseball dataset in
    bb = pd.read_csv(filename)

    # drop the unnecessary columns
    try:
        bb = bb.drop(columns=['Unnamed: 0'])
    except KeyError as e:
        pass

    try:
        bb = bb.drop(columns=['rowid'])
    except KeyError as e:
        pass

    # create dictionary to store results
    """
    constructs and returns a dictionary with the following named cells:
    record.count – count of the number of records in the dataset
    complete.cases – count of the number of complete cases (i.e. records without NAs)
    years – tuple of the form (minimum year, maximum year)
    player.count – count of the number of players (do not double-count)
    team.count – count of the number of teams (do not double-count)
    league.count – count of the number of leagues (do not double-count and do not count “” as a team)
    """
    result = {'record.count': len(bb), 'complete.cases': bb.dropna().shape[0],
              'years': (bb['year'].min(), bb['year'].max()), 'player.count': bb['id'].nunique(),
              'team.count': bb['team'].nunique(), 'league.count': bb.loc[bb['id'] != "", 'lg'].nunique()}

    # calculate the new columns - 'obp' and 'pab'
    """
    baseball data set (data frame) with the following revisions:
    only complete cases (no NaNs)
    Two additional columns:
    obp - on base percentage
    pab - productive at bats percentage
    """
    bb = bb.dropna()
    bb["obp"] = (bb["h"] + bb["bb"] + bb["hbp"]) / (bb["ab"] + bb["bb"] + bb["hbp"])
    bb["pab"] = (bb["h"] + bb["bb"] + bb["hbp"] + bb["sf"] + bb["sh"]) / (
            bb["ab"] + bb["bb"] + bb["hbp"] + bb["sf"] + bb["sh"])
    bb["obp"].replace([np.inf, -np.inf], np.nan, inplace=True)
    bb["pab"].replace([np.inf, -np.inf], np.nan, inplace=True)

    result["bb"] = bb

    # nl - dictionary of national league data
    """
    dat – bb subset consisting of national league (i.e. NL) teams
    players – count of players in the national league data subset
    teams – count of teams in the national league data subset
    """
    nl = {'dat': bb[bb['lg'] == 'NL'],
          'players': bb[bb['lg'] == 'NL']['id'].nunique(),
          'teams': bb[bb['lg'] == 'NL']['team'].nunique()}

    result['nl'] = nl

    # al - dictionary of American league data
    """
    dat – bb subset consisting of American league (i.e. AL) teams
    players – count of players in the American league data subset
    teams – count of teams in the American league data subset
    """
    al = {'dat': bb[bb['lg'] == 'AL'],
          'players': bb[bb['lg'] == 'AL']['id'].nunique(),
          'teams': bb[bb['lg'] == 'AL']['team'].nunique()}

    result['al'] = al

    # create dictionary of records
    """
    dictionary of 14 career records (all determined from players with 50 or more career at bats). Each record is a 
    dictionary containing two items: 1) id – id of player holding record, 2) value – the value of the metric/record 
    (e.g. most homeruns). The 14 records are:
    obp – highest obp (on base percentage)
    pab – highest pab (productive at bats)
    hr – most homeruns 
    hrp – highest homeruns as a percentage of at bats 
    h – most hits 
    hp – highest hits as a percentage of at bats 	
    sb – most stolen bases 
    sbp – highest stolen bases as a percentage of at bats 
    so – most strike outs
    sop – highest strike outs as percentage of at bats
    sopa – highest strike outs as a percentage of plate appearances (at bats, walks, hit by pitch, sacrifice hit, 
    sacrifice fly)
    bb – most walks 
    bbp – highest walks as a percentage of at bats 
    g –most game appearances.
    """
    career = bb.groupby('id').sum().reset_index()
    career['obp'] = (career['h'] + career['bb'] + career['hbp']) / (career['ab'] + career['bb'] + career['hbp'])
    career['pab'] = ((career['h'] + career['bb'] + career['hbp'] + career['sf'] + career['sh']) /
                     (career['ab'] + career['bb'] + career['hbp'] + career['sf'] + career['sh']))
    career["hrp"] = career['hr'] / career['ab']
    career["hp"] = career['h'] / career['ab']
    career["sbp"] = career['sb'] / career['ab']
    career["sop"] = career['so'] / career['ab']
    career["sopa"] = career['so'] / (career['ab'] + career['bb'] + career['hbp'] + career['sf'] + career['sh'])
    career["bbp"] = career['bb'] / career['ab']

    career_records = career[career['ab'] >= 50].reset_index(drop=True)

    records = {}
    for metric in ["obp", "pab", "hr", "hrp", "h", "hp", "sb", "sbp", "so", "sop", "sopa", "bb", "bbp", "g"]:
        max_pos = career_records[metric].idxmax()
        max_row = career_records.iloc[max_pos]
        id = max_row['id']
        value = max_row[metric]
        records[metric] = {"id": id, "value": value}

    result['records'] = records

    # return results

    return result
