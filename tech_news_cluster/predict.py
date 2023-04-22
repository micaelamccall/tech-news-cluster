# from tech_news_cluster.settings import PROJ_ROOT_DIR
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import joblib
import spacy



# Initialize spacy with the english model
sp = spacy.load('en_core_web_sm')

# A function to clean the new string
def clean_string(text_string):
    '''
    A function to clean a string using SpaCy, removing stop-words, non-alphanumeric characters, and pronouns

    Argument: a text string
    Output: a cleaned string

    '''

    # Parse the text string using the english model initialized earlier
    doc = sp(text_string)
    
    # Initialize empty string
    clean = []

    # Add each token to the list if it is not a stop word, is alphanumeric, and if it's not a pronoun
    for token in doc:
        
        if token.is_alpha == False or token.is_stop == True or token.lemma_ == '-PRON-':
            pass
        else:
            clean.append(token.lemma_)

    # Join the list into a string
    clean = " ".join(clean)

    return clean

# Load the models
vectorizer = joblib.load('tech_news_cluster/models/tfidf_vectorizer.sav')

kmeans = joblib.load('tech_news_cluster/models/kmeans.sav')

def predict(input_string = None, filename = None):
    '''
    A function to clean, vectorize, and predict the kmeans cluster of a new string
    
    Arguments: either a string or a filename including extension as a string
    
    Output: a prediction and wordcloud for the document
    '''
    if filename != None:
        with open(os.path.join(PROJ_ROOT_DIR, "content_to_predict", filename), 'r') as file:
            input_string = file.read()
        print('Processing file')
        # Clean the string
        clean = clean_string(input_string)
    
    if input_string != None:
        print('Processing text string')
        clean = clean_string(input_string)
    
    print('String has been cleaned')

    # Vectorize the string
    Y = vectorizer.transform([clean])
    
    print('String has been vectorized')

    # Predict the cluster label
    prediction = kmeans.predict(Y)
    
    # Generate the wordcloud
    cloud = WordCloud().generate(clean)
    
    # Add the prediction to the title of the word cloud
    title = "Cluster Prediction for Article {}".format(prediction)
    
    # Show the word cloud
    plt.figure(figsize = [15,20])
    plt.imshow(cloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title, size =20)
    plt.show();
    
def save_input_string_as_file(input_string, name = 'article_content'):
    PRED_DIR = os.path.join(PROJ_ROOT_DIR, "content_to_predict")
    if not os.path.isdir(PRED_DIR):
        os.makedirs(PRED_DIR)
    with open(os.path.join(PRED_DIR, name + '.txt'), 'w') as file:
        file.write(input_string)




# Test

input_string = '''

A state judge tentatively awarded more than $12.7 million to the 22 women suing porn production company Girls Do Porn today, finding that the company intimidated the women into shooting adult videos, and lied to them about how they will be distributed. The decision follows a years-long legal battle and a 99-day civil trial.

“This outcome is vindication for the many courageous women victimized by GirlsDoPorn, a fraudulent and reprehensible enterprise that thrived on manipulating inexperienced young women,” said Ed Chapin, lead trial counsel, following the ruling.


The women, who are not named in the court case, claimed that the owners and employees of Girls Do Porn lied and manipulated them into shooting adult films on the promise that the content would never be shared widely and that their real names would not be shared. The films were shared within days and weeks immediately after shooting to massive sites like Pornhub and YouPorn. Many of them were viewed millions of times, and many of the women’s real names became public in the comments sections of these videos or on forums dedicated to doxing them.

“Defendants take considerable, calculated steps to falsely assure prospective models that their videos will never be posted online, come to light in the United States, or be seen by anyone who might know them,” Judge Kevin Enright wrote in the decision.

All of the women in the lawsuit testified to being between 17 and 22 when they were first contacted by Girls Do Porn. They were flown to San Diego from all over North America and were put up in hotel rooms with men to shoot a pornographic film, handed dense contracts of legalese to hurriedly sign, and, in some cases were given alcohol and drugs before signing. The judge also found that they were at times threatened until they agreed to sign the contract.

Throughout the trial, the Girls Do Porn defense attorney leaned on these contracts.

“The plaintiffs are adult women who have the responsibility to make adult decisions for themselves, and they must be held responsible for their own decisions and actions,” defense attorney Daniel Kaplan previously said in closing arguments.


Enright disagreed with this assessment. "Defendants rush and pressure the woman to sign the documents quickly without reading them and engage in other deceptive, coercive, and threatening behavior to secure their signatures... The Court finds these putative contracts invalid and unenforceable-part and parcel of Defendants' fraudulent scheme," he wrote in the ruling.

The repercussions from the abuses these women, and potentially hundreds more victims of this company, endured at the coercion of Girls Do Porn affected their entire lives. After they were doxed on sites like Pornhub, where people spread their real names and locations in comment sections and in copies of the films, some women moved across the country, changed their names, and were estranged from their families.

"Defendants are aware that the models recruited for GirlsDoPorn do not intend to pursue a career in adult entertainment," Enright wrote. "The women are mostly students with careers ahead of them who have only even considered Defendants' solicitations to film a pornographic video due to some immediate and pressing financial need."

Each of the 22 plaintiffs was tentatively awarded up to a half million dollars each. While no amount of money will undo what these women have endured for months and years, this is a massive win following a gruelling case that's lasted more than three years.

“After using their multi-million dollar business resources to wage a three-year war of attrition against innocent victims and their counsel, the reprehensible conduct of the defendants is finally exposed and they have been held accountable,” said Brian Holm, attorney for the plaintiffs.

In addition to the money awarded, the court ordered that Girls Do Porn must return all of their images, likenesses, videos, and/or copyrights to the plaintiffs. Much of that content is still online, even though Pornhub has said it has taken steps to delete it.

Girls Do Porn is also prohibited from using, publishing, licensing or distributing the plaintiffs'

images, likenesses, videos or copyrights, and must remove their images, likenesses, or videos from all internet sites owned or controlled by Girls Do Porn, as well as take "active steps" to have such images, likenesses and videos removed from circulation and to safeguard Plaintiffs' privacy.

“The defendants’ conduct before and during this trial was despicable," said John O’Brien, an attorney also representing the plaintiffs. "This case should be a call to lawmakers to enact proactive laws preventing this type of exploitation rather than relying on lawsuits such as this to provide justice to victims.”'''

predict(input_string= input_string)
