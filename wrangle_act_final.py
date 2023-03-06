#!/usr/bin/env python
# coding: utf-8

# # Project: Wrangling and Analyze Data

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import requests as req
import json 
get_ipython().run_line_magic('matplotlib', 'inline')
#importing all the possible extensions that will be useful for the project


# ## Data Gathering
# In the cell below, gather **all** three pieces of data for this project and load them in the notebook. **Note:** the methods required to gather each data are different.
# 1. Directly download the WeRateDogs Twitter archive data (twitter_archive_enhanced.csv)

# In[2]:


TA = pd.read_csv('twitter-archive-enhanced.csv')


# 2. Use the Requests library to download the tweet image prediction (image_predictions.tsv)

# In[3]:


#downloading the twitter images using the requests libary
url = 'https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'
response = req.get(url)
response


# In[4]:


# Saving the dwonloaded image files
open('image-predictions.tsv',mode = 'wb').write(response.content)


# In[5]:


#converting the tsv file into an accesible and readable file in notebooks
images = pd.read_csv('image-predictions.tsv', sep ='\t')


# In[6]:


#viewing(testing the code) the file
images .head()


# 3. Use the Tweepy library to query additional data via the Twitter API (tweet_json.txt)

# In[7]:


import tweepy
from tweepy import OAuthHandler
import json
from timeit import default_timer as timer
#importing the neccessary packages


# In[8]:


# Query Twitter API for each tweet in the Twitter archive and save JSON in a text file
# These are hidden to comply with Twitter's API terms and conditions
consumer_key = 'HIDDEN'
consumer_secret = 'HIDDEN'
access_token = 'HIDDEN'
access_secret = 'HIDDEN'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
#OAuthHander is used for authentication of password without exposing it .

api = tweepy.API(auth, wait_on_rate_limit=True)

# NOTE TO STUDENT WITH MOBILE VERIFICATION ISSUES:
# df_1 is a DataFrame with the twitter_archive_enhanced.csv file. You may have to
# change line 17 to match the name of your DataFrame with twitter_archive_enhanced.csv
# NOTE TO REVIEWER: this student had mobile verification issues so the following
# Twitter API code was sent to this student from a Udacity instructor
# Tweet IDs for which to gather additional data via Twitter's API
df_1 = pd.read_csv('twitter-archive-enhanced.csv')
tweet_ids = df_1.tweet_id.values
len(tweet_ids)

# Query Twitter's API for JSON data for each tweet ID in the Twitter archive
count = 0
fails_dict = {}
start = timer()
# Save each tweet's returned JSON as a new line in a .txt file
with open('tweet_json.txt', 'w') as outfile:
    #The code above saves each tweet returned from the loop into a combined file called 'tweet_json.txt', which can be seen in the file directory.
    # This loop will likely take 20-30 minutes to run because of Twitter's rate limit
    for tweet_id in tweet_ids:
        count += 1
        print(str(count) + ": " + str(tweet_id))
        try:
            tweet = api.get_status(tweet_id, tweet_mode='extended')
            print("Success")
            json.dump(tweet._json, outfile)
            outfile.write('\n')
        except tweepy.errors.TweepyException as e:
            print("Fail")
            fails_dict[tweet_id] = e
            pass
end = timer()
print(end - start)
print(fails_dict)


# # Downloading the json file via url
# The file will be downloaded via a url since twitter refused me a developer account for some unknown reasons.

# In[9]:


url = 'https://video.udacity-data.com/topher/2018/November/5be5fb7d_tweet-json/tweet-json.txt'
response = req.get(url)
response


# In[10]:


#saving the file
open('tweet-json.txt', mode ='wb').write(response.content)


# In[11]:


#reading the downloaded file
twitter_df =[]
with open('tweet-json.txt', 'r') as file:
    lines = file.readlines()
    


# In[12]:


#reading the file line by line
twitter_df =[]
for line in lines:
        parsed_json = json.loads(line)
        twitter_df.append({'tweet_id': parsed_json['id'],
                        'retweet_count': parsed_json['retweet_count'],
                        'favorite_count': parsed_json['favorite_count']})
        
tweet_json = pd.DataFrame(twitter_df, columns = ['tweet_id', 'retweet_count', 'favorite_count'])
    


# In[13]:


#viewing the data
tweet_json.head()


# ## Assessing Data
# In this section, detect and document at least **eight (8) quality issues and two (2) tidiness issue**. You must use **both** visual assessment
# programmatic assessement to assess the data.
# 
# **Note:** pay attention to the following key points when you access the data.
# 
# * You only want original ratings (no retweets) that have images. Though there are 5000+ tweets in the dataset, not all are dog ratings and some are retweets.
# * Assessing and cleaning the entire dataset completely would require a lot of time, and is not necessary to practice and demonstrate your skills in data wrangling. Therefore, the requirements of this project are only to assess and clean at least 8 quality issues and at least 2 tidiness issues in this dataset.
# * The fact that the rating numerators are greater than the denominators does not need to be cleaned. This [unique rating system](http://knowyourmeme.com/memes/theyre-good-dogs-brent) is a big part of the popularity of WeRateDogs.
# * You do not need to gather the tweets beyond August 1st, 2017. You can, but note that you won't be able to gather the image predictions for these tweets since you don't have access to the algorithm used.
# 
# 

# # ASSESSING THE VARIOUS DATAFRAMES VISUALLY
# #  FOR TA dataframe

# In[14]:


TA.info()


# In[15]:


TA.head()


# In[16]:


TA.tail()


# In[17]:


TA.duplicated().sum()


# In[18]:


TA.tweet_id.duplicated().sum()


# # # Value counts function will be used on individual columns to get an idea of how many occurences of unique variables we have for each variable 

# In[19]:


TA.timestamp.value_counts()


# In[20]:



#double checking to make sure the dataframe does nt contain any data 2018
print('2018' in TA['timestamp'].unique())


# In[21]:


TA.rating_denominator.value_counts()


# In[22]:


TA.rating_numerator.value_counts()


# In[23]:


TA.source.value_counts()


# In[24]:


TA.doggo.value_counts()


# In[25]:


TA.floofer.value_counts()


# In[26]:


TA.pupper.value_counts()


# In[27]:


TA.puppo.value_counts()


# In[28]:


TA.retweeted_status_id.value_counts().sum()


# In[29]:


TA.retweeted_status_user_id.value_counts().sum()


# In[30]:


TA.rating_denominator.isna().sum()


# OBSERVATIONS
# 1. There are ridiculously  very high values such as 204,1776,960,666,143,182,144,88,84,165,60,50,44,26,24,80,75,420, in the numerator column and 2333 for the denominator column which makes no sense
# 2. The timestamp column is in string format should be in date time and +0000 will have to be removed
# 3. columns such as text, retweets and replies ,retweeted_status_id,retweeted_status_user_id,retweeted_status_timestamp do not appear to be useful to the analysis since the analysis should involve only original tweets ,hence  should be dropped.
# 4. The floofer, pupper,puppo,doggo columns should all be in a column since they are nick-names of dogs.
# 5. in_reply_to_status_id,in_reply_to_user_id,retweeted_status_id,retweeted_status_user_id,retweeted_status_timestamp have a staggering amount of nulls.
# 6. Dog names in the name column have many variables that are not dog names

# #  ASSESMENT FOR IMAGES DATAFRAME

# In[31]:


images.head()


# In[32]:


images.tail()


# In[33]:


images.info()


# In[34]:


images.duplicated().sum()


# In[35]:


images.jpg_url.duplicated().sum()


# In[36]:


images.isnull().sum()


# In[37]:


images.describe()


# In[38]:


pd.get_option('display.max_rows', None)
#to display more rows


# In[39]:


images.p1


#  we will be using value_counts again to single out unique variables

# In[40]:


images.img_num.value_counts()


# #As seen in the cell above, we have 31 occurences for the variable '4' in the dataframe, 
# those 31 occurences means there are 31 rows of data that do not fall into the most confident category for dog breed analysis , hence they will not be useful to the analysis.

# In[41]:


images.p1_dog.value_counts()


# In[42]:


images.p2_dog.value_counts()


# In[43]:


images.p3_dog.value_counts()


# The 3 cells above shows that there are 543(p1_dog),522(p2_dog) and 576(p3_dog) that the neural network does not identify as dogs and hence should not be used for the analysis.

# In[44]:


images.p1.value_counts()


# In[45]:


images.p2.value_counts()


# In[46]:


images.p3.value_counts()


# OBSERVATIONS
# 1. Some entries are not actually dog breeds, we are having entries such as banana, paper towel,bagel, orange, spatula, etc.
# 2. Presence of duplicate image urls
# 3. There are no null values, which is a good thing.
# 4. The capitalization in the p- columns are inconsistent.
# 5. There are 31 occurences in the datarame that do not fall into the most confident prediction for dog breed analysis
# 

# #  ASSESSMENT FOR TWEET_JSON DATAFRAME

# In[47]:


tweet_json


# In[48]:


tweet_json.info()


# In[49]:


tweet_json.tweet_id.value_counts().sum()


# In[50]:


tweet_json.retweet_count.value_counts()


# In[51]:


tweet_json.isna().sum()


# OBSERVATION
# 1.The tweet_json dataframe have a similar column named tweet_id and hence should be joined to the Twitter_archive(TA) dataframe

# # SUMMARY OF OBSERVATIONS :
# 
# OBSERVATIONS FOR TA(TWITTER ARCHIVE) DATAFRAME
# 1. There are ridiculously  very high values such as 204,1776,960,666,143,182,144,88,84,165,60,50,44,26,24,80,75,420, in the numerator column and 2333 for the denominator column which makes no sense
# 2. The timestamp column is in string format should be in date time and +0000 will have to be removed
# 3. Dropping irrelevant Columns(in_reply_to_status_id,in_reply_to_user_id,retweeted_status_id,retweeted_status_user_id,retweeted_status_timestamp.), thcolumns also happen to have a staggering amount of null values and hence should be deleted because they are strings and the null values cant be made up for. 
# 4. The floofer, pupper,puppo,doggo columns should all be in a column since they are dog-stages of dogs.
# 5. Name column is full of variables that are not dog names
# 
# 
# OBSERVATIONS FOR IMAGES(TWITTER IMAGES)DATAFRAME
# 1. Some entries are not actually dog names, we are having entries such as banana, paper towel,bagel, orange, spatula, etc.
# 2. Presence of duplicate image urls
# 3. There are no null values, which is a good thing.
# 4. The capitalization in the p- columns are inconsistent.
# 5. There are 31 occurences in the datarame that do not fall into the most confident prediction for dog breed analysis
# 6. There are 543(p1_dog),522(p2_dog) and 576(p3_dog) false values that the neural network does not identify as dogs and hence should not be used for the analysis.
# 
# OBSERVATION FOR tweet_json dataframe
# 1.The tweet_json dataframe have a similar column named tweet_id and hence should be joined to the Twitter_archive(TA) dataframe

# # Quality issues
# 
# ## twitter_archive(TA) dataframe
# 1. There are ridiculously  very high values such as 204,1776,960,666,143,182,144,88,84,165,60,50,44,26,24,80,75,420, in the numerator column and 2333 for the denominator column which makes no sense
# 2. The timestamp column is in string format should be in date time and +0000 will have to be removed
# 3. columns such as text, source,retweets and replies ,retweeted_status_id,retweeted_status_user_id,retweeted_status_timestamp do not appear to be useful to the analysis since the analysis should involve only original tweets ,hence  should be dropped.
# 4. in_reply_to_status_id,in_reply_to_user_id,retweeted_status_id,retweeted_status_user_id,retweeted_status_timestamp have a staggering amount of nulls.
# 5. Name column is full of variables that are not dog names
# 
# ## images dataframe
# 1. Some entries are not actually dog breeds, we are having entries such as banana, paper towel,bagel, orange, spatula, etc.
# 2. Presence of duplicate image urls
# 3. There are 31 occurences in the datarame that do not fall into the most confident prediction for dog breed analysis.
# 4. Grouping the p1, p2, p3 columns into one since they are all dog breeds, it makes more sense to have them in a column .
# 5. The p1_conf, p2_conf and p3_conf levels should all be in a column.
# 6. The capitalization in the p- columns are inconsistent.
# 

# # Tidiness issues
# 
# ## twitter_archive(TA) dataframe
# 1. The floofer, pupper,puppo,doggo columns should all be in a column since they are nick-names of dogs.
# 
# # images dataframe  
# 2. The images,twitter archive and tweet_json dataframes should all be combined into a dataframe.
# 

# ## Cleaning Data
# In this section, clean **all** of the issues you documented while assessing. 
# 
# **Note:** Make a copy of the original data before cleaning. Cleaning includes merging individual pieces of data according to the rules of [tidy data](https://cran.r-project.org/web/packages/tidyr/vignettes/tidy-data.html). The result should be a high-quality and tidy master pandas DataFrame (or DataFrames, if appropriate).

# In[52]:


# Make copies of original pieces of data
clean_TA = TA.copy()
clean_images = images.copy()
clean_tweet_jason = tweet_json.copy()
clean_TA


# # QUALITY ISSUES

# ## TWITTER ARCHIVE DF
# 
# ### Issue #1: DROPPING IRRELEVANT COLUMNS TO THE ANALYSIS
# The columns that are irrelevant involves all related to retweets , since we are meant to keep only originals, they include;
# in_reply_to_status_id,
# in_reply_to_user_id,
# retweeted_status_id,
# retweeted_status_timestamp,
# retweeted_status_user_id,source and expanded_urls.
# #### And deletion of rows with non null values for either retweeted status id or retweeted user status id columns

# ### Deletion of rows with non null values either retweeted status id or retweeted user status id columns

# ### DEFINE: A subset of the dataframe containing only rows with retweet values will be created using notnull() function and deleted using their indexes via a drop function.

# In[53]:


clean_TA.retweeted_status_id.notnull().sum()
#to check how many rows 


# In[54]:


#displaying all the rows to allow for better visual assessment and understanding
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


# In[55]:


clean_TA.retweeted_status_timestamp.notnull().sum()
#creating a subset of the dataframe
retweets_rows = clean_TA.loc[clean_TA['retweeted_status_id'].notnull()]


# In[56]:


list(retweets_rows.index.values)
#list of index to be used for deleting rows with retweet


# #### Dropping the rows using the indexes

# In[57]:


#clean_TA =clean_TA.drop((retweets_rows.index.values),inplace = True)
clean_TA = clean_TA.drop([19,32,36,68,73,74,78,91,95,97,101,109,118,124,130,132,137,146,155,159,160,165,171,180,182,185,194,195,204,211,
               212,222,230,231,247,250,260,266,272,273,281,285,286,289,298,302,303,307,309,310,319,327,332,340,341,343,357,
               359,366,382,386,397,399,406,411,415,420,422,425,431,434,435,438,446,447,450,453,455,462,465,469,475,476,479,485,
               488,506,522,530,535,538,541,543,546,552,555,558,561,566,568,574,577,581,583,586,589,594,595,596,597,598,599,
               600,601,602,603,604,605,606,612,615,618,627,629,634,654,655,656,661,664,669,671,677,682,686,692,694,702,720,
               728,741,742,745,749,753,759,764,767,770,773,778,784,794,800,811,815,818,822,826,829,833,841,847,860,868,872,885,
               890,895,908,911,926,937,943,949,1012,1023,1043,1242,2259,2260],inplace =False)


# In[58]:


clean_TA.retweeted_status_id.notnull().sum()


# #### Define 2: the drop function will be used to delete the columns at once

# #### Code

# In[59]:


clean_TA = clean_TA.drop(['in_reply_to_status_id', 
                            'in_reply_to_user_id',
                            'retweeted_status_id',
                            'retweeted_status_user_id',
                            'retweeted_status_timestamp','expanded_urls','source'],axis=1)


# #### Test

# In[60]:


clean_TA.head()
#it worked!!..yeee!!


# In[ ]:





# # ISSUE 2:
# ## IMAGES DATAFRAME(DF):
# ### Grouping the p1, p2, p3 columns into one since they are all dog breeds, it makes more sense to have them in a column  and deletion of variables that are not dog breeds after applying the melt

# ### DEFINE: The melt function will be used to unpivot  the columns and pivot them into one column and a drop function will be used to delete the intermediate column.

# ### CODE:

# In[61]:


clean_images


# In[62]:


clean_images = pd.melt(clean_images, 
                    id_vars = [ 'tweet_id','jpg_url','img_num','p1_conf','p1_dog','p2_conf','p2_dog','p3_conf','p3_dog'],
                                value_vars = ['p1', 'p2', 'p3'], 
                                var_name = 'p1-p3', 
                                value_name = 'dog_breed')


# ### TEST :

# In[63]:


clean_images.head()


# In[64]:


# DRopping the old column(p1-p3)
clean_images.drop('p1-p3', axis = 1, inplace = True)


# In[65]:


#checking for columns to see if the drop worked
clean_images.columns


# In[66]:


#checking for duplicates
clean_images.tweet_id.duplicated().sum()


# In[67]:


clean_images.drop_duplicates("tweet_id",inplace = True)


# In[68]:


#test
clean_images.tweet_id.duplicated().sum()


# In[69]:


clean_images.head(20)


# ### TEST :

# ### DELETION OF NON DOG BREEDS IN THE NEWLY FORMED DOG BREED COLUMN

# In[70]:


#assessing the df before deleting the non dog breeds in the dog breed column

clean_images.head()


# In[71]:


#to see each unique value in the dog_breed column
clean_images.dog_breed.value_counts()


# From the cell above and below, it is seen that we have alot of absurd values that are not dog breeds, we will have to delete all such rows of data , to have a clean data set.
# To do this, we have to create a list of all the entries that are not dog breeds by going through eah row.
# Upon close observation, dog breed entrieds with a value count of 60 and below are not dog entries

# ### A loop will be created to use in deleting the non breeds of dogs after creating a list of the non dogs.Its still alot of work though.

# In[73]:



#creation of list
non_dogs = ['neck_brace','steam_locomotive','wild_boar','cradle','hen','stone_wall','canoe','waffle_iron','crutch',
            'paper_towel','snorkel','indian_elephant','barrel','wig','mitten','snowmobile','shovel','purse',
           'aschan','window_screen','chimpanzee','comic_book','prison','bookshop','red_wolf','loafer','box_turtle','christmas_stocking','television',
'minivan','sulphur-crested_cockatoo','jaguar','monitor','oxygen_mask','binder','Loggerhead','vacuum','vacuum','indri','consomme','lion',
'lion','tripod','shoji','studio_couch','soap_dispenser','handkerchief','bighorn','squirrel_monkey','bolete','bathtub','refrigerator',
'limousine','limousine','cup','dishwasher','junco','minibus','guinea_pig','persian_cat','swing','tennis_ball','bath_towel','bath_towel',
'white_wolf','ice_bear',"jack-o-'-lantern",'hay','zebra','african_hunting_dog','hyena','toyshop','hog','weasel','arctic_fox','toilet_tissue',
'hog','web_site','bathtub','shopping_cart','muzzle','sea_lion','seat_belt','doormat','beaver','rain_barrel','crib','pretzel','power_drill',
'leafhopper','leafhopper','hair_spray','plow','home_theater','remote_control','paintbrush','tabby','shower_curtain','greenhouse','hatchet',
'spatula','crossword_puzzle','can_opener','bagel','stove','piggy_bank','seashore','wool','tiger_cat','street_sign','hair_slide','rapeseed',
'fountain','radiator','loupe','bouvier_des_flandres','window_shade','panpipe','military_uniform','mashed_potato','mosquito_net','crate',
'hippopotamus','terrapin','golfcart','grocery_store','chest','sorrel','coyote','earthstar','computer_keyboard','snow_leopard','bannister',
'buckeye','hotdog','syringe','carousel','chain_saw','bow','hand_blower','quill','table_lamp','black-footed_ferret','koala','hamster',
'tub','feather_boa','sunglasses','wallaby','brown_bear','sombrero','cougar','ski_mask','gibbon','water_buffalo','fur_coat','shopping_basket',
'quilt','car_mirror','racket','dhole','goose','sandbar','wombat','bubble','ram','swab','book_jacket','jack-o-lantern','giant_panda','pillow',
'american_black_bear','soccer_ball','polecat','space_heater','toilet_seat','dogsled','cowboy_boot','grey_fox','bucket','acorn_squash',
'hare','king_penguin','mongoose','shower_cap','timber_wolf','basketball','paddle','leatherback_turtle','affenpinscher','carton','bathing_cap',
'toyshop','hyena','arabian_camel','barrow','macaque','cowboy_hat','meerkat','sleeping_bag','three-toed_sloth','bonnet','bow_tie','maillot',
'maillot','Sea_lion','conch','Wood_rabbit','menu','ox','corn','skunk','marmot','sock','mouse','tricycle','washbasin','Poncho','Wok','egyptian_cat',
'sliding_door','oscilloscope','mousetrap','nipple','academic_gown','bathtub','hamster','tub','swing','guinea_pig','muzzle','sea_lion','weasel',
'arabian_camel','koala','toilet_tissue','ram','black-footed-ferret','sunglasses','shopping_cart','ox','badger','badger','fountain','jigsaw_puzzle',
'quilt','sandbar','carton','minivan','feather_boa','sandbar','fur_coat','prison','paper_towel','barber_chair','stingray','crash_helmet',
'lifeboat','cockroach','grey_whale','toucan','lynx','candle','tiger','bobsled','accordion','tarantula','sulphur_butterfly','siamang','tray',
'breastplate','orangutan','folding_chair','sandal','promontory','sarong','coral_fungus','European_gallinule','police_van','tree_frog',
'banded_gecko','leaf_beetle','suit','horse_cart','quail','medicine_chest','go-kart','apron','cannon','streetcar','trench_coat','trombone',
'ping-pong_ball','spotted_salamander','knee_pad','toaster','pelican','hamper','cornet','spotlight','drake','lorikeet','coffeepot','grille',
'revolver','pole','barracouta','desk','armadillo','torch','spindle','turnstile','Gila_monster','chain_mail','breakwater','solar_dish',
'barbershop','lesser_panda','great_grey_owl','patridge','dock','projectile','dumbell','rule','pencil_box','sweatshirt','lighter','necklace',
'ipod','dam','confectionery','volcano','saltshaker','gar','washer','leopard','coho','fire_engine','lacewing','flamingo','microphone',
'pitcher','pitcher','bee_eater','starfish','screen','robin','dumbbell','patridge','acorn','jeep','African_chamelon','Band_Aid','French_horn',
'balance_beam','bulletproof_vest','wooden_spoon','wing','cardoon','wolf_spider','stinkhorn','drumstick','plastic_bag','African_crocodile',
'African_grey','agama','alp','American_black_bear','Arabian_camel','Arctic_fox','axolotl','bakery','bald_eagle','balloon','banana','barbell',
'beach_wagon','bearskin','bib','binoculars','birdhouse','bison','boathouse','bookcase','cash_machine','cheeseburger','cheetah','china_cabinet',
'Christmas_stocking','cliff','clog','coffee_mug','coil','clumber','common_iguana','convertible','coral_reef','crane','cuirass','damselfly',
'desktop_computer','dining_table','dough','Egyptian_cat','electric_fan','envelope','espresso','fiddler_crab','four-poster','frilled_lizard',
'gas_pump','geyser','gondola','guenon','hammer','harp','hermit_crab','hummingbird','ibex',"jack-o'-lantern",'jellyfish','jersey','killer_whale',
'lakeside','laptop','lawn_mower','llama','Loafer','long-horned_beetle','Madagascar_cat','mailbox','maze','microwave','motor_scooter','mud_turtle',
'nail','ocarina','orange','ostrich','otter','padlock','park_bench','patio','peacock','pedestal','pool_table','porcupine','pot','prayer_rug',
'radio_telescope','redbone','restaurant','school_bus','scorpion','sea_urchin','shield','Siamese_cat','slug','snail','sundial','tailed_frog',
'teapot','tick','tiger_shark','traffic_light','triceratops','tusker','upright','walking_stick','water_bottle','wood_rabbit','platypus']

#creation of the loops to use in deleting the non dogs
for breed in non_dogs:
    clean_breeds = clean_images[(clean_images['dog_breed'] == breed)].index
    clean_images.drop(clean_breeds, inplace=True)


# In[75]:


#testing 
(clean_images['dog_breed'].eq('tick')).any()


# In[76]:


#testing 
clean_images.dog_breed.value_counts()


# In[77]:


#testing 
#we can use any of the words in quotes from the cell above
(clean_images['dog_breed'].eq('jeep')).any()


# In[78]:


clean_images


# The spreadsheet clean up worked, as it can be seen above after using value counts for the dog breed column, there are no more values that are not dog breeds.

# ## ISSUE 3:

# #### Twitter_archive DF :
# #### Deletion of Non dog names in the Name column

# ### Define:
# Upon observation the variables in the Name column are  all  lower case , and this can be used to filter them and delete them

# In[79]:


#obtaining the frequency of the variables and sorting them 
mask = clean_TA.name.str.contains('^[a-z]', regex = True)
clean_TA[mask].name.value_counts().sort_index()


# In[80]:


not_dogs = ['a','actually','all','an','by','getting','his','incredibly','infuriating','just','life','light','mad','my','not',
            'officially','old','one','quite','space','such','the','this','unacceptable','very']


# In[81]:


clean_TA = clean_TA[~clean_TA.isin(not_dogs)]


# In[82]:


### TEST:
clean_TA.name


# In[83]:


clean_TA.name.value_counts()
#VALUE COUNTS TO SHOW ALL THE VARIABLES IN THE NAME COLUMN


# # Issue 4:
# ## TA(twitter_archive) DF;
# 
# ### FIXING ABNORMALLY HIGH VALUES FOR THE RATING  DENOMINATOR COLUMNS
# 

# ### Define:
# Upon observation of the text column, it can be seen that the coulumn also contains ratings in the text.
# To solve the incorrect rating issue, denominators not equal to 10 will be filtered away using the query function and then the correct ratings will be inserted into the columns.

# In[84]:


pd.set_option('display.max_colwidth', -1) # to have a complete display of the column details
clean_TA.text


# ### code: 

# In[85]:


abnormal_denominator = clean_TA.query('rating_denominator != 10')
abnormal_denominator.rating_denominator
#for easy access and display of the required columns


# In[86]:


abnormal_denominator.text


# In[87]:



# Correct ratings by reading through the text, most of the abnormal ratings are associated with multiple dogs.
# tweet_id: 666287406224695296
clean_TA.loc[clean_TA.tweet_id == 666287406224695296, 'rating_numerator'] = 9
clean_TA.loc[clean_TA.tweet_id == 666287406224695296, 'rating_denominator'] = 10


# In[88]:


# tweet_id: 697463031882764288 --- Multiple dogs
clean_TA.loc[clean_TA.tweet_id == 697463031882764288, 'rating_numerator'] = 11
clean_TA.loc[clean_TA.tweet_id == 697463031882764288, 'rating_denominator'] = 10

# tweet_id: 684222868335505415 --- Multiple dogs
clean_TA.loc[clean_TA.tweet_id == 684222868335505415, 'rating_numerator'] = 11
clean_TA.loc[clean_TA.tweet_id == 684222868335505415, 'rating_denominator'] = 10

# tweet_id: 682962037429899265 
clean_TA.loc[clean_TA.tweet_id == 682962037429899265, 'rating_numerator'] = 10
clean_TA.loc[clean_TA.tweet_id == 682962037429899265, 'rating_denominator'] = 10

# tweet_id: 710658690886586372 --- Multiple dogs
clean_TA.loc[clean_TA.tweet_id == 710658690886586372, 'rating_numerator'] = 10
clean_TA.loc[clean_TA.tweet_id == 710658690886586372, 'rating_denominator'] = 10

# tweet_id: 713900603437621249 --- Multiple dogs
clean_TA.loc[clean_TA.tweet_id == 713900603437621249, 'rating_numerator'] = 11
clean_TA.loc[clean_TA.tweet_id == 713900603437621249, 'rating_denominator'] = 10

# tweet_id: 709198395643068416 --- Multiple dogs
clean_TA.loc[clean_TA.tweet_id == 709198395643068416, 'rating_numerator'] = 9
clean_TA.loc[clean_TA.tweet_id == 709198395643068416, 'rating_denominator'] = 10

# tweet_id: 722974582966214656 
clean_TA.loc[clean_TA.tweet_id == 722974582966214656, 'rating_numerator'] = 13
clean_TA.loc[clean_TA.tweet_id == 722974582966214656, 'rating_denominator'] = 10

# tweet_id: 716439118184652801
clean_TA.loc[clean_TA.tweet_id == 716439118184652801, 'rating_numerator'] = 11
clean_TA.loc[clean_TA.tweet_id == 716439118184652801, 'rating_denominator'] = 10

# tweet_id: 704054845121142784 --- Multiple dogs
clean_TA.loc[clean_TA.tweet_id == 704054845121142784, 'rating_numerator'] = 12
clean_TA.loc[clean_TA.tweet_id == 704054845121142784, 'rating_denominator'] = 10

# tweet_id: 677716515794329600 --- Multiple dogs
clean_TA.loc[clean_TA.tweet_id == 677716515794329600, 'rating_numerator'] = 12
clean_TA.loc[clean_TA.tweet_id == 677716515794329600, 'rating_denominator'] = 10

# tweet_id: 675853064436391936 --- Multiple dogs
clean_TA.loc[clean_TA.tweet_id == 675853064436391936, 'rating_numerator'] = 11
clean_TA.loc[clean_TA.tweet_id == 675853064436391936, 'rating_denominator'] = 10

# tweet_id: 810984652412424192  no rating
clean_TA.loc[clean_TA.tweet_id == 810984652412424192, 'rating_numerator'] = 10
clean_TA.loc[clean_TA.tweet_id == 810984652412424192, 'rating_denominator'] = 10

# tweet_id: 820690176645140481 --- Multiple dogs
clean_TA.loc[clean_TA.tweet_id == 820690176645140481, 'rating_numerator'] = 12
clean_TA.loc[clean_TA.tweet_id == 820690176645140481, 'rating_denominator'] = 10

# tweet_id: 731156023742988288 --- Multiple dogs
clean_TA.loc[clean_TA.tweet_id == 731156023742988288, 'rating_numerator'] = 12
clean_TA.loc[clean_TA.tweet_id == 731156023742988288, 'rating_denominator'] = 10

# tweet_id: 758467244762497024 --- Multiple dogs
clean_TA.loc[clean_TA.tweet_id == 758467244762497024, 'rating_numerator'] = 11
clean_TA.loc[clean_TA.tweet_id == 758467244762497024, 'rating_denominator'] = 10

# tweet_id: 740373189193256964
clean_TA.loc[clean_TA.tweet_id == 740373189193256964, 'rating_numerator'] = 14
clean_TA.loc[clean_TA.tweet_id == 740373189193256964, 'rating_denominator'] = 10

#tweet_id:835246439529840640
clean_TA.loc[clean_TA.tweet_id == 835246439529840640, 'rating_numerator'] = 13
clean_TA.loc[clean_TA.tweet_id == 835246439529840640,  'rating_denominator'] = 10

#tweet_id:775096608509886464
clean_TA.loc[clean_TA.tweet_id == 775096608509886464, 'rating_numerator'] = 14
clean_TA.loc[clean_TA.tweet_id == 775096608509886464, 'rating_denominator'] = 10

#tweet_id:832088576586297345
clean_TA.loc[clean_TA.tweet_id == 832088576586297345, 'rating_denominator'] = 10

#tweet_id:686035780142297088
clean_TA.loc[clean_TA.tweet_id == 686035780142297088, 'rating_denominator'] = 10

#tweet_id:684225744407494656
clean_TA.loc[clean_TA.tweet_id == 684225744407494656, 'rating_denominator'] = 10

#tweet_id:682808988178739200
clean_TA.loc[clean_TA.tweet_id == 682808988178739200, 'rating_denominator'] = 10


# In[89]:


clean_TA.rating_denominator
clean_TA.query('rating_denominator != 10')
#oops!! seems like we were unable to capture all for the denominator column, we will have to run the code above again
#and include the tweet id's below
# we will replace all the denominators , since its meant to be 10, for the numerator we will calculate the mean of the correct
# and replace the absurd values with the mean by creating a new dataframe excluding those ones.


# As seen above after replacing all the denominator values with 10 , there are no more dirty data in the denominator column

# # Issue 5:
# ## TA(twitter_archive) DF;
# 
# ### FIXING ABNORMALLY HIGH VALUES  AND  FOR THE RATING  NUMERTATOR COLUMNS
# 

# In[90]:


#Capturing decimal values in the rating_numerator column
ratings = clean_TA.text.str.extract('((?:\d+\.)?\d+)\/(\d+)', expand=True)


# In[91]:


#removing decimal values
decimals = clean_TA[~clean_TA.isin(ratings)]
#testing the removals
ratings


# In[92]:


clean_TA.query('rating_numerator >20')
#we are using 20 because its not so common to find numerators higher than 20 and it's safe to assume that any one higher than 20 is an error.
# we have quite a number of dirty/ absurd values in the numerator column
# we will create a new dataframe with correct values and calculate the mean, which will be used to replace the absurd values.


# In[93]:


#creating new df
good_numerator =clean_TA.query('rating_numerator < 20')
good_numerator.describe()
good_numerator.rating_numerator.mean()
#the code above calculated the mean of the numeartor and rounded it up to the closest whole number.
#this mean will be used to replace values higher than 20 for the numerator column.
good_mean = good_numerator.rating_numerator.mean()
good_mean = round(good_mean)


# In[94]:


good_mean


# In[95]:


#replacing numerator columns higher than 20 with the loc function

#tweet_id:855862651834028034
clean_TA.loc[clean_TA.tweet_id == 855862651834028034, 'rating_numerator'] = good_mean

#tweet_id:855860136149123072
clean_TA.loc[clean_TA.tweet_id == 855860136149123072, 'rating_numerator'] = good_mean

#tweet_id:838150277551247360
clean_TA.loc[clean_TA.tweet_id == 838150277551247360, 'rating_numerator'] = good_mean

#tweet_id:832215909146226688
clean_TA.loc[clean_TA.tweet_id == 832215909146226688, 'rating_numerator'] = good_mean

#tweet_id:786709082849828864
clean_TA.loc[clean_TA.tweet_id == 786709082849828864, 'rating_numerator'] = good_mean

#tweet_id:778027034220126208
clean_TA.loc[clean_TA.tweet_id == 778027034220126208, 'rating_numerator'] = good_mean

#tweet_id:749981277374128128
clean_TA.loc[clean_TA.tweet_id == 749981277374128128, 'rating_numerator'] = good_mean

#tweet_id:684225744407494656
clean_TA.loc[clean_TA.tweet_id == 684225744407494656, 'rating_numerator'] = good_mean

#tweet_id:680494726643068929
clean_TA.loc[clean_TA.tweet_id == 680494726643068929, 'rating_numerator'] = good_mean

#tweet_id:670842764863651840
clean_TA.loc[clean_TA.tweet_id == 670842764863651840, 'rating_numerator'] = good_mean
clean_TA.loc[clean_TA.tweet_id == 835246439529840640,'rating_numerator'] = good_mean


# In[96]:


bad_numerator =clean_TA.query('rating_numerator > 20')
bad_numerator 
#yeaee!!
#fixed all the absurd numerator


# In[97]:


clean_TA.query('rating_numerator > 20')
clean_TA.query('rating_denominator != 10')


# ### Test

# # Issue 6:
# ## TA(twitter_archive) DF;
# 
# ### CORRECTING THE TIME STAMP COLUMN(The timestamp column is in string format should be in date time and +0000 will have to be removed)

# ### Define:
# 

# To solve this issue we will have to delete the extra 0000 using .str function to delete the extra zeros and use the to_date_time function to convert to date time.

# ### code:

# In[98]:


#deleting the extra zeros
clean_TA.timestamp = clean_TA.timestamp.str[:-6]


# In[99]:


#converting to time date format
clean_TA['timestamp'] =pd.to_datetime(clean_TA['timestamp'])


# #### Test

# In[100]:


clean_TA.timestamp
clean_TA.timestamp.head()
#as can be seen below the dtype is now datetime format


# # Issue 7:
# ## IMAGES DATAFRAME
# 
# ### There are 31 occurences in the dataframe that do not fall into the most confident prediction for dog breed analysis.

# ### Define
# we will drop rows with img_num greater than 3.(ie ; any rows with 4 in it will be deleted)
# #to do this we will create a new temporal dataframe containing only those rows 
# #delete the new dataframe from the main dataframe using the index

# ### code:

# In[101]:


#viewing the rows with a confidence score of > 3
clean_images.query('img_num > 3')


# In[102]:


#creating the dataframe and checking the index
least_confident = clean_images[(clean_images['img_num']> 3)].index
least_confident


# In[103]:


#dropping the temporal dataframe
clean_images.drop(least_confident,inplace = True)


# ### Test:

# In[104]:


clean_images.query('img_num > 3')


# ### As it can be seen in the cell above there are no more values higher than 3 in the img_num column

# # Issue 8:
# ## Images Dataframe:
# ## Presence of duplicate image url's in the jpg_url column.

# ## Define:
# The duplicates images url will be dropped using drop_duplicates function, specifically targeting the jpg_url column

# # code :

# In[105]:


duplicates =clean_images[clean_images.jpg_url.duplicated()]
duplicates.jpg_url.value_counts().sum()
clean_images.shape


# In[106]:


#Delete duplicate rows based on jpg_url column 
#df2 = df.drop_duplicates(subset=["Courses", "Fee"], keep=False)
clean_images.drop_duplicates("jpg_url",inplace =True)


# ### Test:

# In[107]:


clean_images.shape


# AS seen above the number of rows has decreased from 1533 to 1481

# In[108]:


clean_images


# # Issue 9 : Images Dataframe
# ## :Inconsistent capitalization in the p columns.( now dog_breeds)
# ## . 

# ### DEFINE:
# The str.capitalize funtion will be used to capitalize the first letters of the columns

# In[109]:


clean_images.dog_breed = clean_images.dog_breed.str.capitalize()


# ### Test:

# In[110]:


clean_images.dog_breed.head()


# The code worked. The first letter of every word in the column is now capitalized as seen from the snippet of the column above

# # ISSUES 10:
# ## IMAGES DF:
# ## The p1_conf, p2_conf and p3_conf levels should all be in a column

# ### Define :
# ### Melt function will be used to create a new column called confident levels and the old columns will be deleted using  a drop function

# ### Code:

# In[111]:


clean_images= pd.melt(clean_images,
                      id_vars = ['tweet_id','jpg_url','img_num','p1_dog','p2_dog','p3_dog','dog_breed'],
                     value_vars =['p1_conf','p2_conf','p3_conf'],
                     var_name ='p-configs',
                     value_name ='confidence_levels')


# In[112]:


## testing if the melt function worked.
clean_images.columns


# In[113]:


#dropping the var_name (P-configs)
clean_images.drop('p-configs',axis = 1, inplace = True)


# In[114]:


#testing if the drop worked
clean_images.columns


# In[115]:


#checking for duplicates
clean_images.tweet_id.duplicated().sum()


# In[116]:


#dropping the duplicates
clean_images.drop_duplicates('tweet_id',inplace= True)


# In[117]:


#testing the drop
clean_images.tweet_id.duplicated().sum()


# ### TEST:

# In[118]:


clean_images.columns
clean_images.head()


# # TIDINESS ISSUES

# # ISSUE 1
# ### TWITTER ARCHIVE (TA) DF :
# #### The floofer, pupper,puppo,doggo columns should all be in a column since they are nick-names of dogs.

# ## Define:
#  

# In[119]:


#Replacing none values with a space and then commas in the columns
clean_TA.doggo.replace('None', '', inplace=True)
clean_TA.floofer.replace('None','', inplace = True)
clean_TA.pupper.replace('None','', inplace =True)
clean_TA.puppo.replace('None','', inplace =True)


# In[120]:


#creation of the new column via concatenation
clean_TA['dog_stage'] = clean_TA.doggo + clean_TA.floofer + clean_TA.pupper + clean_TA.puppo
clean_TA.loc[clean_TA.dog_stage == 'doggopupper', 'dog_stage'] = 'doggo, pupper'
clean_TA.loc[clean_TA.dog_stage == 'doggopuppo', 'dog_stage'] = 'doggo, puppo'
clean_TA.loc[clean_TA.dog_stage == 'doggofloofer', 'dog_stage'] = 'doggo, floofer'


# clean_TA.head()
# clean_TA = pd.melt(clean_TA, 
#                     id_vars = ['tweet_id', 'timestamp', 'text', 'expanded_urls', 'rating_numerator', 'rating_denominator', 'name'],
#                                 value_vars = ['doggo', 'floofer', 'pupper', 'puppo'], 
#                                 var_name = 'dog_types',
#                                 value_name = 'dog_stage', )

# clean_TA.dog_types.value_counts()
# clean_TA.dog_types

# In[121]:


clean_TA.columns
#to display all the columns in the dataframe


# In[122]:


clean_TA


# In[123]:


clean_TA.tweet_id.duplicated().sum()


# In[124]:


#dropping the doggo,floofer.puppo and pupper columns since they are already in the dog stages column.
clean_TA.drop(['doggo','floofer','pupper','puppo'],axis = 1,inplace =True)


# # ISSUES 2:
# ### COMBINING THE THREE DATAFRAMES INTO ONE.

# ### Define : To carry this out, a pandas.merge function will be used to concat the three tables together. Before appplying the merge function, the datframes will be viewed to get a proper understanding of the position of the primary key.

# ### code:

# ### Aseessing the data frames before joining :

# In[125]:


clean_TA.info()


# In[126]:


#testing the change of data types
clean_images.info()


# In[127]:


clean_tweet_jason.info()


# In[128]:


#converting the tweet_id column into integers like the other dataframes before merging
clean_images['tweet_id'] = clean_images['tweet_id'].astype(np.int64)


# ### After examination of the three dataframes, the primary key is the tweet_id and we will be merging the dataframes using that column.

# In[129]:


# joining the tweet_jason df to twitter archive df
TA_FT= pd.merge(clean_tweet_jason,clean_TA)
TA_FT


# In[130]:


clean_images.info()


# In[131]:


final_df =pd.merge(TA_FT,clean_images, how ='inner')
final_df


# ### Assessing the new dataframe

# In[132]:


final_df.info()


# In[133]:


final_df.shape


# ## Storing Data
# Save gathered, assessed, and cleaned master dataset to a CSV file named "twitter_archive_master.csv".
# PS:
# (I actually prefer using twitter_dogs)

# In[134]:


# Store the clean dataframe in a CSV file named twitter_archive_master.csv
final_df.to_csv('twitter_archive_master.csv',index= False)


# In[135]:


# load data and view
df = pd.read_csv('twitter_archive_master.csv')
df.head(5)


# ## Analyzing and Visualizing Data
# In this section, analyze and visualize your wrangled data. You must produce at least **three (3) insights and one (1) visualization.**

# ### Insights:
# 1. Dog breeds with the highest ratings
# 
# 2. Most popular dog breeds: This can be calculated based on the engagement of the tweet, number of tweets,retweets and likes(favs) 
# 
# 3. Accuracy of the predictions made by checking if there is a positive correlation between the img_num column and the confidence levels columns.
# 4. Dog breeds with Least ratings.

# ## INSIGHT 1
# ### Accuracy of the predictions made.
# The img_num column is an indication of how confident the neural network prediction is, ideally as the confidence value increases, the img_num  is supposed to decrease(an indication of a confident prediction).
# This can be analyzed by plotting a scatterplot of img_num against the confidence levels columns.

# In[136]:


df.img_num.mean()


# In[137]:


df.confidence_levels.mean() 


# In[138]:


base_color = sn.color_palette()[4]
sn.regplot(data= df, x = 'img_num',y = 'confidence_levels', color = base_color).set(title = 'Correlation of confidence levels and img_num');
plt.gca().invert_xaxis()


# ### The scatterplot above shows the relationship between neural newtwork prediction and the confidence levels,it can be seen that there is an decrease in the confidence levels  as the img_num value  increases(1 is the most precise prediction and 3 the least precise) and this simply means that the accuracy of the neural network declines. Because a higher img_num means a less accurate prediction.

# ### INSIGHT 2:
# ### Most Popular Dog breeds

# In[139]:


#most popular dog breeds based on number of tweets
df.dog_breed.value_counts()[10::-1].plot(kind = 'barh',x= 'count',y ='dog_breed', title = 'Top 10 Popular Dog Dreeds Based On number of Tweets');


# In[140]:


#Most popular dogs based on retweets and favourit counts
# creation of the dataframe that will be used,involving only certain columns
columns = ['dog_breed', 'retweet_count', 'favorite_count']
df_breed = df[columns]

breed_retweet = df_breed.groupby('dog_breed')['retweet_count'].agg('sum').sort_values(ascending=False)[10::-1]
breed_favorite = df_breed.groupby('dog_breed')['favorite_count'].agg('sum').sort_values(ascending=False)[10::-1]

# Plot horizontal bar chart
fig, (ax1, ax2) = plt.subplots(2, 1)

# Top 10 breeds based on number of retweets
breed_retweet.plot.barh(ax=ax1, figsize=(8,12), color='#6A6ACD')
ax1.set_title("Top 10 Breeds Based On Retweets Count")

# Top 10 breeds based on number of favorite
breed_favorite.plot.barh(ax=ax2, color='#2E8B58')
ax2.set_title("Top 10 Breeds Based on Favorite Count")

fig.subplots_adjust(hspace=0.5)


# The five most popular dog breeds based on tweets,retweets and favorite counts are the golden_retriever(no 1),labrador_retriever(no2),pembroke(no3),chihuahua(no4) and samoyed(no 5).These breeds constantly topped the charts as can be seen from the plots above.Positions 1-4 was constantly dominated by the dog_breeds holding the positions across the 3 parameters used for the analysis.The samoyed breed was the 5th most popular dog based on the retweets and favorites counts , but not tweets.Although it came in at no 7 based on tweets.
# These plots reveals that these dog breeds are highly popular and most talked/tweeted about amongst twitter users

# #### 

# ## INSIGHT 3:
# ####  DOG BREED WITH HIGHESET RATINGS.
# ### This can be calculated by taking the numerator ratings for each of the dog breeds and grouped by the dog_breeds column.

# In[141]:


# Make a list of top popular dog breeds based on number of tweets
top_tweet_count = df.dog_breed.value_counts().sort_values(ascending=False).nlargest(10).rename_axis('dog_breed').reset_index(name='tweet_counts')
breed_list = top_tweet_count.dog_breed.tolist()
# Average rating for top breeds based on number of tweets
avg_rating = df.groupby('dog_breed').rating_numerator.mean().sort_values(ascending=False).rename_axis('breed').reset_index(name='avg_rating')
breed_avg_rating = avg_rating[avg_rating['breed'].isin(breed_list)]
breed_avg_rating


# Once again,for dogs with highest ratings amongst twitter users, we have a list similar to the popularity list earlier. The samoyed breed has the highest rating followed by the chow breed,golden retriever, pembroke,labrador retriever, toy_poodle , malamute, chihuahua and pug. The dog breeds with highest ratings all have at least appeared once in the most popular breeds contest using the retweets, tweets and favorite counts.
# This arouses a new insight : is there any correlation between ratings and popularity?

# In[142]:


breed_avg_rating.plot(kind='bar', x='breed', y='avg_rating')  
plt.title(' Dog Breeds With Highest Ratings')
plt.ylabel("Average_rating")
plt.xlabel("Breed");


# ### INSIGHT 4 : 
# DOG BREEDS WITH LEAST RATINGS

# In[143]:


# Make a list of least popular dog breeds based on number of tweets
top_tweet_count = df.dog_breed.value_counts().sort_values(ascending=False).nsmallest(10).rename_axis('dog_breed').reset_index(name='tweet_counts')
breed_list = top_tweet_count.dog_breed.tolist()
# Average rating for top breeds based on number of tweets
avg_rating = df.groupby('dog_breed').rating_numerator.mean().sort_values(ascending=True).rename_axis('breed').reset_index(name='least_avg_rating')
breed_avg_rating = avg_rating[avg_rating['breed'].isin(breed_list)]

breed_avg_rating


# The dog breed with least rating is the japanese_spaniel followed by the african hunting dog and  scotch terrier with a tie in number 2. 

# ### LIMITATIONS:
# #### The dataset used for the analysis does not have any control standards, and this greatly affects how null or abnormal values for the ratings will be treated. It makes it alot less accuarate and alot more difficult for manipulation.
# #### The absence of a standard list of known dog breeds makes the cleaning process more tasking. I think a list of all known dog breeds should have been provided , in order to make the cleaning process for the dog breeds easy

# # references
# https://sparkbyexamples.com/pandas/pandas-convert-string-column-to-datetime/#:~:text=Use%20pandas%20to_datetime()%20function,string%20you%20wanted%20to%20convert.
# 
# https://www.geeksforgeeks.org/drop-rows-from-the-dataframe-based-on-certain-condition-applied-on-a-column/
# https://sparkbyexamples.com/pandas/pandas-merge-multiple-dataframes-2/
# https://stackoverflow.com/questions/16424493/pandas-setting-no-of-max-rowsk
# https://www.geeksforgeeks.org/how-to-drop-rows-that-contain-a-specific-value-in-pandas/
# https://stackoverflow.com/questions/18172851/deleting-dataframe-row-in-pandas-based-on-column-value
# https://stackoverflow.com/questions/43269548/pandas-how-to-remove-rows-from-a-dataframe-based-on-a-list
# https://github.com/Monicajhe/Wrangle-and-Analyze-Data/blob/master/wrangle_act.ipynb
# https://seaborn.pydata.org/examples/part_whole_bars.html

# In[ ]:





# In[ ]:




