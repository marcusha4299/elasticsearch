# elasticsearch

/////////////////////////////////////////////////////////////////////////////////////////////////////

Milestone 1: Building the inverted index 

Now that you have been provided the HTML files to index, you may build your               
inverted index off of them. The inverted index is simply a map with the token                
as a key and a list of its corresponding postings. A posting is the representation
of the token’s occurrence in a document. The posting typically (not limited to)
contains the following info (you are encouraged to think of other attributes that
you could add to the index):



• The document name/id the token was found in.

• Its tf-idf score for that document (for MS1, add only the term frequency).

Some tips:
• When designing your inverted index, you will think about the structure
of your posting first.

• You would normally begin by implementing the code to calculate/fetch
the elements which will constitute your posting.

• Modularize. Use scripts/classes that will perform a function or a set of
closely related functions. This helps in keeping track of your progress,
debugging, and also dividing work amongst teammates if you’re in a group.

• We recommend you use GitHub as a mechanism to work with your team
members on this project, but you are not required to do so.

////////////////////////////////////////////////////////////////////////////////////////////////////






/////////////////////////////////////////////////////////////////////////////////////////////////////

Milestone 2: Develop a search and retrieval component

At least the following queries should be used to test your retrieval:
1 cristina lopes
2 machine learning
3 ACM
4 master of software engineering

Developing the Search component:

• Once you have built the inverted index, you are ready to test document retrieval
with queries. At the very least, the search should be able to deal with boolean
queries: AND only.

• If you wish, you can sort the retrieved documents based on tf-idf scoring
(you are not required to do so now, but doing it now may save you time in
the future). This can be done using the cosine similarity method. Feel free to
use a library to compute cosine similarity once you have the term frequencies
and inverse document frequencies (although it should be very easy for you to
write your own implementation). You may also add other weighting/scoring
mechanisms to help refine the search results.

Submit your code and a report (in pdf) to Canvas with the following content:
• the top 5 URLs for each of the queries above
• a picture of your search interface in action

//////////////////////////////////////////////////////////////////////////////////////////////////////
