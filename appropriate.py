import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="GenAI Selection Tool",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.25rem solid #1f77b4;
    }
    .recommendation-box {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 2px solid #1f77b4;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 0.25rem solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_requirements' not in st.session_state:
    st.session_state.user_requirements = {}

# Title and introduction
st.title("🤖 GenAI Embedding & Vector Database Selection Tool")
st.markdown("### Find the perfect combination for your AI application")
st.markdown("---")

# Sidebar for requirements gathering
st.sidebar.header("📋 Define Your Requirements")

# Requirement collection
domain = st.sidebar.selectbox(
    "Application Domain",
    ["General Text", "Code Search", "Scientific/Medical", "E-commerce", "Legal Documents", "Multi-language", "Multimodal (Text+Images)"]
)

data_volume = st.sidebar.selectbox(
    "Expected Data Volume",
    ["Small (< 1M vectors)", "Medium (1M-10M vectors)", "Large (10M-100M vectors)", "Very Large (> 100M vectors)"]
)

latency_req = st.sidebar.selectbox(
    "Latency Requirements",
    ["Ultra-fast (< 10ms)", "Fast (10-50ms)", "Moderate (50-200ms)", "Flexible (> 200ms)"]
)

query_volume = st.sidebar.selectbox(
    "Expected Query Volume",
    ["Low (< 1K/day)", "Medium (1K-100K/day)", "High (100K-1M/day)", "Very High (> 1M/day)"]
)

budget = st.sidebar.selectbox(
    "Budget Preference",
    ["Cost-Optimized", "Balanced", "Performance-First"]
)

team_expertise = st.sidebar.selectbox(
    "Team Technical Expertise",
    ["Beginner", "Intermediate", "Expert"]
)

deployment = st.sidebar.selectbox(
    "Deployment Preference",
    ["Cloud/Managed", "On-Premise", "Hybrid", "No Preference"]
)

special_features = st.sidebar.multiselect(
    "Required Features",
    ["Real-time Updates", "Hybrid Search", "Multi-tenancy", "Advanced Filtering", "GDPR Compliance", "High Availability"]
)

# Store requirements
st.session_state.user_requirements = {
    'domain': domain,
    'data_volume': data_volume,
    'latency': latency_req,
    'query_volume': query_volume,
    'budget': budget,
    'expertise': team_expertise,
    'deployment': deployment,
    'features': special_features
}

# Main content area with tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Recommendations", "🧮 Embedding Models", "🗄️ Vector Databases", "📈 Comparison", "🎯 Decision Matrix"])

with tab1:
    st.header("🎯 Personalized Recommendations")
    
    # Recommendation logic based on user inputs
    def get_embedding_recommendations(requirements):
        recommendations = []
        
        if requirements['domain'] == "Code Search":
            recommendations.append({
                'model': 'CodeBERT',
                'score': 95,
                'reason': 'Specifically designed for code understanding',
                'dimensions': 768,
                'speed': 'Medium',
                'cost': 'Free'
            })
            recommendations.append({
                'model': 'text-embedding-ada-002',
                'score': 85,
                'reason': 'Excellent general performance, good with code',
                'dimensions': 1536,
                'speed': 'Fast',
                'cost': '$0.0001/1K tokens'
            })
        elif requirements['domain'] == "Scientific/Medical":
            recommendations.append({
                'model': 'BioBERT',
                'score': 95,
                'reason': 'Domain-specific training on biomedical texts',
                'dimensions': 768,
                'speed': 'Medium',
                'cost': 'Free'
            })
            recommendations.append({
                'model': 'SciBERT',
                'score': 90,
                'reason': 'Trained on scientific literature',
                'dimensions': 768,
                'speed': 'Medium',
                'cost': 'Free'
            })
        elif requirements['domain'] == "Multimodal (Text+Images)":
            recommendations.append({
                'model': 'CLIP',
                'score': 95,
                'reason': 'Joint text-image understanding',
                'dimensions': 512,
                'speed': 'Medium',
                'cost': 'Free'
            })
        else:
            # General recommendations
            if requirements['budget'] == "Cost-Optimized":
                recommendations.append({
                    'model': 'all-MiniLM-L6-v2',
                    'score': 85,
                    'reason': 'Excellent performance-to-size ratio',
                    'dimensions': 384,
                    'speed': 'Very Fast',
                    'cost': 'Free'
                })
            elif requirements['budget'] == "Performance-First":
                recommendations.append({
                    'model': 'text-embedding-ada-002',
                    'score': 95,
                    'reason': 'State-of-the-art performance',
                    'dimensions': 1536,
                    'speed': 'Fast',
                    'cost': '$0.0001/1K tokens'
                })
            else:
                recommendations.append({
                    'model': 'all-mpnet-base-v2',
                    'score': 90,
                    'reason': 'Great balance of performance and speed',
                    'dimensions': 768,
                    'speed': 'Fast',
                    'cost': 'Free'
                })
        
        return sorted(recommendations, key=lambda x: x['score'], reverse=True)
    
    def get_vectordb_recommendations(requirements):
        recommendations = []
        
        volume = requirements['data_volume']
        expertise = requirements['expertise']
        deployment = requirements['deployment']
        
        if volume == "Small (< 1M vectors)":
            if expertise == "Beginner":
                recommendations.append({
                    'database': 'Chroma',
                    'score': 95,
                    'reason': 'Easy setup, perfect for small scale',
                    'managed': 'Self-hosted',
                    'cost': 'Free',
                    'setup_difficulty': 'Easy'
                })
            else:
                recommendations.append({
                    'database': 'FAISS',
                    'score': 90,
                    'reason': 'High performance for small-medium datasets',
                    'managed': 'Self-hosted',
                    'cost': 'Free',
                    'setup_difficulty': 'Medium'
                })
        
        elif "Large" in volume:
            if deployment == "Cloud/Managed":
                recommendations.append({
                    'database': 'Pinecone',
                    'score': 95,
                    'reason': 'Proven scalability, managed service',
                    'managed': 'Fully Managed',
                    'cost': '$70-$500+/month',
                    'setup_difficulty': 'Easy'
                })
            else:
                recommendations.append({
                    'database': 'Milvus',
                    'score': 90,
                    'reason': 'Open source, highly scalable',
                    'managed': 'Self-hosted',
                    'cost': 'Infrastructure only',
                    'setup_difficulty': 'Hard'
                })
        
        else:  # Medium volume
            recommendations.append({
                'database': 'Qdrant',
                'score': 92,
                'reason': 'Great performance, rich features',
                'managed': 'Both available',
                'cost': 'Free/Paid cloud',
                'setup_difficulty': 'Medium'
            })
            recommendations.append({
                'database': 'Weaviate',
                'score': 88,
                'reason': 'Feature-rich, good documentation',
                'managed': 'Both available',
                'cost': 'Free/Paid cloud',
                'setup_difficulty': 'Medium'
            })
        
        return sorted(recommendations, key=lambda x: x['score'], reverse=True)
    
    # Get recommendations
    embedding_recs = get_embedding_recommendations(st.session_state.user_requirements)
    vectordb_recs = get_vectordb_recommendations(st.session_state.user_requirements)
    
    # Display recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧮 Recommended Embedding Models")
        for i, rec in enumerate(embedding_recs[:3]):
            with st.container():
                st.markdown(f"""
                <div class="recommendation-box">
                    <h4>#{i+1} {rec['model']} (Score: {rec['score']})</h4>
                    <p><strong>Why:</strong> {rec['reason']}</p>
                    <p><strong>Dimensions:</strong> {rec['dimensions']} | <strong>Speed:</strong> {rec['speed']} | <strong>Cost:</strong> {rec['cost']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("🗄️ Recommended Vector Databases")
        for i, rec in enumerate(vectordb_recs[:3]):
            with st.container():
                st.markdown(f"""
                <div class="recommendation-box">
                    <h4>#{i+1} {rec['database']} (Score: {rec['score']})</h4>
                    <p><strong>Why:</strong> {rec['reason']}</p>
                    <p><strong>Type:</strong> {rec['managed']} | <strong>Cost:</strong> {rec['cost']} | <strong>Setup:</strong> {rec['setup_difficulty']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Combined recommendation
    st.markdown("---")
    st.subheader("🎯 Optimal Combination")
    if embedding_recs and vectordb_recs:
        best_embedding = embedding_recs[0]
        best_vectordb = vectordb_recs[0]
        
        st.markdown(f"""
        <div class="recommendation-box">
            <h3>🏆 Recommended Stack</h3>
            <h4>Embedding: {best_embedding['model']} + Vector DB: {best_vectordb['database']}</h4>
            <p><strong>Expected Performance:</strong> High accuracy with {best_embedding['speed'].lower()} embedding speed</p>
            <p><strong>Scalability:</strong> Suitable for your {st.session_state.user_requirements['data_volume'].lower()} requirement</p>
            <p><strong>Total Setup Time:</strong> ~{2 if best_vectordb['setup_difficulty'] == 'Easy' else 5 if best_vectordb['setup_difficulty'] == 'Medium' else 10} days</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.header("🧮 Embedding Models Comparison")
    
    # Comprehensive embedding models data
    embedding_data = {
        'Model': [
            'text-embedding-ada-002', 'all-MiniLM-L6-v2', 'all-mpnet-base-v2',
            'all-distilroberta-v1', 'multilingual-e5-large', 'CodeBERT',
            'BioBERT', 'SciBERT', 'CLIP', 'sentence-t5-base'
        ],
        'Dimensions': [1536, 384, 768, 768, 1024, 768, 768, 768, 512, 768],
        'Max_Tokens': [8191, 256, 384, 512, 512, 512, 512, 512, 77, 512],
        'Domain': [
            'General', 'General', 'General', 'General', 'Multilingual',
            'Code', 'Biomedical', 'Scientific', 'Multimodal', 'General'
        ],
        'Cost': [
            '$0.0001/1K tokens', 'Free', 'Free', 'Free', 'Free',
            'Free', 'Free', 'Free', 'Free', 'Free'
        ],
        'Speed_Score': [85, 95, 80, 85, 70, 75, 75, 75, 80, 75],
        'Accuracy_Score': [95, 82, 88, 85, 90, 92, 95, 94, 90, 83],
        'Memory_MB': [2000, 80, 420, 290, 2000, 500, 420, 420, 350, 850],
        'License': [
            'Commercial', 'Apache 2.0', 'Apache 2.0', 'Apache 2.0', 'MIT',
            'Apache 2.0', 'Apache 2.0', 'Apache 2.0', 'MIT', 'Apache 2.0'
        ],
        'Best_For': [
            'Production RAG', 'Fast prototyping', 'Balanced performance', 'Sentence similarity',
            'Multilingual apps', 'Code search', 'Medical documents', 'Research papers',
            'Image-text search', 'Text generation'
        ]
    }
    
    df_embeddings = pd.DataFrame(embedding_data)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        domain_filter = st.selectbox("Filter by Domain", ["All"] + list(df_embeddings['Domain'].unique()))
    with col2:
        cost_filter = st.selectbox("Filter by Cost", ["All", "Free Only", "Paid Only"])
    with col3:
        sort_by = st.selectbox("Sort by", ["Accuracy_Score", "Speed_Score", "Dimensions", "Memory_MB"])
    
    # Apply filters
    filtered_df = df_embeddings.copy()
    if domain_filter != "All":
        filtered_df = filtered_df[filtered_df['Domain'] == domain_filter]
    if cost_filter == "Free Only":
        filtered_df = filtered_df[filtered_df['Cost'] == 'Free']
    elif cost_filter == "Paid Only":
        filtered_df = filtered_df[filtered_df['Cost'] != 'Free']
    
    filtered_df = filtered_df.sort_values(sort_by, ascending=False)
    
    # Display table
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Speed_Score": st.column_config.ProgressColumn(
                "Speed Score",
                help="Higher is faster",
                min_value=0,
                max_value=100,
            ),
            "Accuracy_Score": st.column_config.ProgressColumn(
                "Accuracy Score",
                help="Higher is more accurate",
                min_value=0,
                max_value=100,
            ),
            "Memory_MB": st.column_config.NumberColumn(
                "Memory (MB)",
                help="Memory usage in MB"
            )
        }
    )
    
    # Visualization
    st.subheader("📈 Performance Comparison")
    
    fig = px.scatter(
        filtered_df,
        x='Speed_Score',
        y='Accuracy_Score',
        size='Memory_MB',
        color='Domain',
        hover_data=['Model', 'Dimensions', 'Cost'],
        title="Speed vs Accuracy (Bubble size = Memory Usage)"
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("🗄️ Vector Database Comparison")
    
    # Comprehensive vector database data
    vectordb_data = {
        'Database': [
            'Pinecone', 'Weaviate', 'Qdrant', 'Milvus', 'Chroma',
            'FAISS', 'Elasticsearch', 'Redis', 'MongoDB Atlas', 'Vespa'
        ],
        'Type': [
            'Managed', 'Both', 'Both', 'Both', 'Self-hosted',
            'Self-hosted', 'Both', 'Both', 'Managed', 'Self-hosted'
        ],
        'Max_Vectors': [
            '100M+', '100M+', '100M+', '1B+', '10M',
            '1B+', '50M', '100M', '100M+', '1B+'
        ],
        'Query_Speed_Score': [95, 85, 90, 88, 80, 98, 75, 90, 70, 92],
        'Setup_Difficulty': [1, 6, 5, 8, 2, 4, 7, 5, 3, 9],
        'Cost_Score': [60, 80, 85, 90, 100, 100, 70, 75, 65, 95],
        'Features_Score': [85, 95, 90, 85, 70, 60, 80, 75, 75, 95],
        'Real_Time_Updates': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes'],
        'Hybrid_Search': ['Yes', 'Yes', 'Yes', 'Yes', 'No', 'No', 'Yes', 'No', 'Yes', 'Yes'],
        'Multi_Tenancy': ['Yes', 'Yes', 'Yes', 'Yes', 'No', 'No', 'Yes', 'Yes', 'Yes', 'Yes'],
        'Open_Source': ['No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Partial', 'Partial', 'No', 'Yes'],
        'Best_For': [
            'Production RAG', 'Feature-rich apps', 'High performance', 'Large scale',
            'Prototyping', 'Research/Local', 'Text search', 'Real-time apps',
            'Enterprise', 'Complex queries'
        ],
        'Monthly_Cost_USD': [70, 25, 20, 0, 0, 0, 80, 50, 57, 0]
    }
    
    df_vectordb = pd.DataFrame(vectordb_data)
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        type_filter = st.selectbox("Service Type", ["All"] + list(df_vectordb['Type'].unique()))
    with col2:
        opensource_filter = st.selectbox("Open Source", ["All", "Yes", "No"])
    with col3:
        budget_max = st.number_input("Max Monthly Budget ($)", min_value=0, max_value=1000, value=1000)
    with col4:
        sort_vectordb = st.selectbox("Sort by", ["Query_Speed_Score", "Features_Score", "Cost_Score", "Setup_Difficulty"])
    
    # Apply filters
    filtered_vectordb = df_vectordb.copy()
    if type_filter != "All":
        filtered_vectordb = filtered_vectordb[filtered_vectordb['Type'] == type_filter]
    if opensource_filter != "All":
        filtered_vectordb = filtered_vectordb[filtered_vectordb['Open_Source'] == opensource_filter]
    filtered_vectordb = filtered_vectordb[filtered_vectordb['Monthly_Cost_USD'] <= budget_max]
    filtered_vectordb = filtered_vectordb.sort_values(sort_vectordb, ascending=(sort_vectordb == 'Setup_Difficulty'))
    
    # Display table
    st.dataframe(
        filtered_vectordb,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Query_Speed_Score": st.column_config.ProgressColumn(
                "Speed Score",
                min_value=0,
                max_value=100,
            ),
            "Features_Score": st.column_config.ProgressColumn(
                "Features Score",
                min_value=0,
                max_value=100,
            ),
            "Cost_Score": st.column_config.ProgressColumn(
                "Cost Score",
                help="Higher = more cost effective",
                min_value=0,
                max_value=100,
            ),
            "Setup_Difficulty": st.column_config.ProgressColumn(
                "Setup Difficulty",
                help="Lower = easier to setup",
                min_value=1,
                max_value=10,
            ),
            "Monthly_Cost_USD": st.column_config.NumberColumn(
                "Monthly Cost ($)",
                format="$%d"
            )
        }
    )
    
    # Radar chart for comparison
    st.subheader("🎯 Multi-dimensional Comparison")
    selected_dbs = st.multiselect(
        "Select databases to compare (max 5)",
        df_vectordb['Database'].tolist(),
        default=df_vectordb['Database'].tolist()[:3]
    )
    
    if selected_dbs:
        # Create radar chart
        categories = ['Query Speed', 'Features', 'Cost Effectiveness', 'Ease of Setup']
        
        fig = go.Figure()
        
        for db in selected_dbs[:5]:  # Limit to 5 for readability
            db_data = df_vectordb[df_vectordb['Database'] == db].iloc[0]
            values = [
                db_data['Query_Speed_Score'],
                db_data['Features_Score'],
                db_data['Cost_Score'],
                100 - db_data['Setup_Difficulty'] * 10  # Invert difficulty for radar
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=db
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Vector Database Comparison Radar Chart"
        )
        
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("📈 Performance & Cost Analysis")
    
    # Create performance comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Embedding Models: Speed vs Accuracy")
        fig1 = px.scatter(
            df_embeddings,
            x='Speed_Score',
            y='Accuracy_Score',
            color='Domain',
            size='Dimensions',
            hover_data=['Model', 'Memory_MB'],
            title="Choose models in top-right quadrant"
        )
        fig1.add_hline(y=85, line_dash="dash", annotation_text="Good Accuracy Threshold")
        fig1.add_vline(x=80, line_dash="dash", annotation_text="Good Speed Threshold")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Vector DBs: Performance vs Cost")
        fig2 = px.scatter(
            df_vectordb,
            x='Cost_Score',
            y='Query_Speed_Score',
            color='Type',
            size='Features_Score',
            hover_data=['Database', 'Monthly_Cost_USD'],
            title="Higher cost score = more cost effective"
        )
        fig2.add_hline(y=85, line_dash="dash", annotation_text="Good Performance")
        fig2.add_vline(x=80, line_dash="dash", annotation_text="Good Value")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Cost breakdown
    st.subheader("💰 Total Cost of Ownership Calculator")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        monthly_queries = st.number_input("Monthly Queries (millions)", min_value=0.1, max_value=1000.0, value=1.0)
    with col2:
        selected_embedding = st.selectbox("Embedding Model", df_embeddings['Model'].tolist())
    with col3:
        selected_vectordb = st.selectbox("Vector Database", df_vectordb['Database'].tolist())
    
    # Calculate costs
    embedding_cost = 0
    if selected_embedding == 'text-embedding-ada-002':
        embedding_cost = monthly_queries * 1000 * 0.0001  # $0.0001 per 1K tokens
    
    vectordb_cost = df_vectordb[df_vectordb['Database'] == selected_vectordb]['Monthly_Cost_USD'].iloc[0]
    if vectordb_cost == 0:  # Self-hosted
        vectordb_cost = monthly_queries * 10  # Estimated infrastructure cost
    
    total_cost = embedding_cost + vectordb_cost
    
    # Display cost breakdown
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Embedding Cost", f"${embedding_cost:.2f}/month")
    with col2:
        st.metric("Vector DB Cost", f"${vectordb_cost:.2f}/month")
    with col3:
        st.metric("Total Monthly Cost", f"${total_cost:.2f}")
    with col4:
        st.metric("Cost per Query", f"${total_cost/(monthly_queries*1000000):.6f}")

with tab5:
    st.header("🎯 Decision Matrix")
    
    st.markdown("### Use this decision tree to quickly narrow down your choices:")
    
    # Decision tree logic
    def show_decision_path():
        st.markdown("""
        ```
        📊 DECISION TREE
        
        1. What's your data volume?
           ├── < 1M vectors
           │   ├── Beginner team → Chroma + all-MiniLM-L6-v2
           │   └── Experienced → FAISS + all-mpnet-base-v2
           │
           ├── 1M-10M vectors
           │   ├── Need managed service → Pinecone + text-embedding-ada-002
           │   └── Self-hosted → Qdrant + all-mpnet-base-v2
           │
           └── > 10M vectors
               ├── Budget focused → Milvus + all-MiniLM-L6-v2
               └── Performance focused → Pinecone + text-embedding-ada-002
        
        2. Special requirements?
           ├── Code search → CodeBERT + Weaviate
           ├── Scientific → SciBERT + Milvus
           ├── Multimodal → CLIP + Weaviate
           └── Multilingual → multilingual-e5-large + Qdrant
        
        3. Latency critical?
           ├── < 10ms → FAISS + all-MiniLM-L6-v2
           └── < 50ms → Pinecone + text-embedding-ada-002
        ```
        """)
    
    show_decision_path()
    
    # Interactive decision matrix
    st.subheader("🔍 Interactive Requirements Matrix")
    
    # Create a scoring system
    requirements = {
        'Performance': st.slider("Performance Priority (1-10)", 1, 10, 8),
        'Cost': st.slider("Cost Sensitivity (1-10)", 1, 10, 6),
        'Ease of Use': st.slider("Ease of Use Priority (1-10)", 1, 10, 7),
        'Scalability': st.slider("Scalability Need (1-10)", 1, 10, 5),
        'Features': st.slider("Advanced Features Need (1-10)", 1, 10, 6)
    }
    
    # Calculate weighted scores for each combination
    def calculate_score(embedding, vectordb, weights):
        # Simplified scoring logic
        embedding_scores = {
            'text-embedding-ada-002': {'Performance': 10, 'Cost': 3, 'Ease': 9, 'Scale': 10, 'Features': 8},
            'all-MiniLM-L6-v2': {'Performance': 7, 'Cost': 10, 'Ease': 10, 'Scale': 8, 'Features': 6},
            'all-mpnet-base-v2': {'Performance': 8, 'Cost': 9, 'Ease': 9, 'Scale': 8, 'Features': 7}
        }
        
        vectordb_scores = {
            'Pinecone': {'Performance': 10, 'Cost': 4, 'Ease': 10, 'Scale': 10, 'Features': 8},
            'Chroma': {'Performance': 6, 'Cost': 10, 'Ease': 10, 'Scale': 5, 'Features': 5},
            'Qdrant': {'Performance': 9, 'Cost': 8, 'Ease': 7, 'Scale': 9, 'Features': 9}
        }
        
        total_score = 0
        for key, weight in weights.items():
            short_key = key.split()[0]  # Get first word
            if short_key == 'Ease':
                short_key = 'Ease'
            elif short_key == 'Scalability':
                short_key = 'Scale'
            elif short_key == 'Features':
                short_key = 'Features'
            
            total_score += (embedding_scores.get(embedding, {}).get(short_key, 5) + 
                           vectordb_scores.get(vectordb, {}).get(short_key, 5)) * weight
        
        return total_score / 2  # Average
    
    # Calculate scores for top combinations
    combinations = [
        ('text-embedding-ada-002', 'Pinecone'),
        ('all-MiniLM-L6-v2', 'Chroma'),
        ('all-mpnet-base-v2', 'Qdrant')
    ]