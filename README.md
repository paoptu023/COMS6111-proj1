# COMS E6111 Project 1
* Group name: Project 1 Group 23
 * Qi Wang (qw2197), Yongjia Huo (yh2796)

* Submitted files:
 * main.py – the main program, get relevance feedback
 * parameters.py – parameter settings and parser
 * query_processor.py – implement the Rocchio algorithm
 * stopwords.txt – list of stop words
 * transcript.txt
 * README.md

* Use the following command to run our program:
 * python main.py &lt;account key&gt; &lt;target precision&gt; &lt;initial query&gt;
 * For example, python main.py 'HIWkFhlcqfV0SsO9ac7smysylCtGDsuMVyqgSWPPDZI' 1 'musk'

* Description of design:
 * Each query round we display the URL, title and description of top-10 results returned from the Bing Search API, and prompt user to mark each page as relevant or not relevant. We parse the text from description into a list of words split by spaces, then we use all terms not in the stop words list to construct the vector space. Title and URL are not considered because compound words tend to appear in title and URL, making the query results unstable. We use the Rocchio algorithm and tf-idf to calculate term weights, the two highest-weighted terms not presented in last query are added in the new query, terms in new query are ordered by their weights. Each round we calculate the precision@10, if the target value is achieved or the precision is zero, the program terminates.

* Description of query-modification method:
 * For each query, we add results marked as relevant into the relevant set, and results marked as nor-relevant to non-relevant set. Then we replace all punctuations in the description with white spaces, convert the string into lower characters and split it into a bunch of words. Stop words are removed. 

 * After parsing, we calculate the term frequency of relevant documents, term frequency of non-relevant documents and document frequency respectively. Then we construct the document vector using the Rocchio algorithm, the term weight of document vector is calculated by tf-idf algorithm: W(ij) = TF(ij) * log(#documents / DF(i))

 * The vector is sorted decreasingly by term weights. Finally, we add weights to terms in old query, the two new terms of highest weights are considered good candidates for query expansion and appended to the old query.

* Bing Search Account Key: HIWkFhlcqfV0SsO9ac7smysylCtGDsuMVyqgSWPPDZI

* References:
 * Singhal, Amit. "Modern information retrieval: A brief overview." IEEE Data Eng. Bull. 24.4 (2001): 35-43.
 * Christopher D. Manning, Prabhakar Raghavan, and Hinrich Schütze. 2008. Introduction to Information Retrieval. Cambridge University Press, New York, NY, USA.


