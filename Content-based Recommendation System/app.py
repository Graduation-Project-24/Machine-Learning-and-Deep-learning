# app.py

from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Load data and models
def load_models():
    global main_feature4m_df, cosine_sim
    main_feature4m_df = pd.read_csv('cleaned_data_v5.csv')
    cosine_sim = np.load('cosine_sim11.npy')

load_models()

def content_based_recommendations(product_id: int, data: pd.DataFrame, cosine_sim: np.ndarray, n: int = 5):
    """
    Generate content-based recommendations based on product_id.
    
    Parameters:
    - product_id: The ID of the product to base recommendations on.
    - data: DataFrame containing the product data.
    - cosine_sim: Precomputed cosine similarity matrix.
    - n: Number of recommendations to generate.
    
    Returns:
    - A tuple of DataFrame with recommended products and their similarity scores.
    """
    try:
        idx = data[data['product_id'] == product_id].index[0]
    except IndexError:
        raise HTTPException(status_code=404, detail="Product ID not found")
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]
    product_indices = [i[0] for i in sim_scores]
    
    # return a list of recommended product_id, product_name, rating, rating_count, discounted_price, actual_price, category_1, category_2, img_link_y
    return data.iloc[product_indices][['product_id', 'product_name', 'rating', 'rating_count', 'discounted_price', 'actual_price', 'category_1', 'category_2', 'img_link_y', 'sale_rate']], sim_scores

@app.get("/", tags=["Home"])
def api_home():
    """
    Home endpoint to check API status.
    """
    return {'detail': 'Welcome to FastAPI TextGen Tutorial!'}

@app.post("/api/recommendations", summary="Generate recommendations based on product ID", tags=["Recommendations"])
def get_recommendations(product_id: int, num_recommendations: int = 5):
    """
    Generate product recommendations based on the provided product ID.
    
    Parameters:
    - request: RecommendationRequest object containing product_id and num_recommendations.
    
    Returns:
    - JSON response with recommended product IDs and their similarity scores.
    """
    recommendations, sim_scores = content_based_recommendations(
        product_id, main_feature4m_df, cosine_sim, num_recommendations
    )
    return {
        'product_id': product_id,
        'recommendations': recommendations.to_dict(orient='records'),
        'similarity_scores': sim_scores
    }

@app.get("/api/best_selling", summary="Get best selling products", tags=["Best Selling"])
def get_best_selling(n: int = 3):
    """
    Get the best selling products.
    
    Parameters:
    - n: Number of best selling products to return.
    
    Returns:
    - JSON response with best selling products.
    """
    best_selling = main_feature4m_df.sort_values('rating_count', ascending=False).head(n)
    return best_selling.to_dict(orient='records')

@app.get("/api/new_arrivals", summary="Get new arrivals", tags=["New Arrivals"])
def get_new_arrivals(n: int = 5):
    """
    Get the new arrivals.
    
    Parameters:
    - n: Number of new arrivals to return.
    
    Returns:
    - JSON response with new arrival products.
    """
    most_sale_rate = main_feature4m_df.sort_values('sale_rate', ascending=False).head(n)
    return most_sale_rate.to_dict(orient='records')

# recommendations = get_recommendations(22, 5)
# print(recommendations)
# print('---------------------------------')
# best_selling = get_best_selling(3)
# print(best_selling)
# print('---------------------------------')
# new_arrivals = get_new_arrivals(5)
# print(new_arrivals)


# https://esmael-saleh-recommend-50-samples.hf.space/docs


# to run the app on swagger ui:
# run the app.py file
# go to http://127.0.0.1:7860/docs