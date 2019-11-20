# Statute Recommendation Based on Word Embedding
Graduation Project in Nanjing University
## Summary 
* Researched and proposed an improved weighted minimum edit distance algorithm for statute standardization.
* Applied Word Mover’s Distance algorithm to measure similarity between legal documents.
* Trained a model for recommending associated statutes based on document similarity and achieved **80% accuracy**.
### WMD
* Used *jieba* library to split Chinese texts
* Used *word2vec* to train word vector models
* Applied **Word Mover’s Distance** algorithm to compute the similarity between legal documents
* Recommended the statutes that need to be quoted based on the most similar legal documents
* Verified recommendation results
