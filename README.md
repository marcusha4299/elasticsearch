# elasticsearch

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
