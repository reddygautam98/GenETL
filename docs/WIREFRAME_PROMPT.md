# GenETL Wireframe Generation Prompt

## 🎨 Design Brief for GenETL AI-Enhanced ETL Platform

Create comprehensive wireframes for GenETL, an AI-powered ETL (Extract, Transform, Load) data platform that combines traditional data processing with advanced artificial intelligence capabilities. The platform should feel modern, intuitive, and professional while showcasing its powerful AI features.

## 📋 Platform Overview

**GenETL** is an enterprise-grade data platform that features:
- **5 Core AI Components**: AI Insights Generator, Smart Data Quality AI, AI Query Interface, Predictive Analytics Engine, AI Report Generator
- **Traditional ETL Infrastructure**: Apache Airflow, PostgreSQL, Redis
- **Target Users**: Data Engineers, Data Analysts, Business Users, Data Scientists, Business Leaders
- **Key Value Proposition**: Transform complex data operations into intelligent, automated workflows

## 🎯 Design Requirements

### Design Philosophy
- **AI-First**: Emphasize intelligent automation and insights
- **User-Centric**: Intuitive interface for both technical and business users
- **Modern Enterprise**: Professional, clean, scalable design
- **Data-Driven**: Rich visualizations and clear data presentation
- **Responsive**: Works across desktop, tablet, and mobile devices

### Brand Guidelines
- **Primary Colors**: 
  - AI Blue: #017CEE (Trust, Intelligence)
  - Data Green: #28a745 (Success, Growth)
  - Insight Orange: #fd7e14 (Innovation, Energy)
- **Secondary Colors**:
  - Dark Navy: #1e2746 (Professional, Stable)
  - Light Gray: #f8f9fa (Background, Clean)
  - Warning Amber: #ffc107 (Attention, Alerts)
- **Typography**: Modern sans-serif (Inter, Roboto, or similar)
- **Icons**: Outlined style, consistent with AI/data themes

## 🏠 Main Dashboard Wireframe

### Header Navigation
```
[GenETL Logo] [AI Dashboard] [ETL Pipelines] [Data Sources] [Reports] [Settings] [User Profile]
                   Active
```

### Main Content Area
```
┌─────────────────────────────────────────────────────────────────────┐
│ Welcome back, [User Name]                                    [🔔][⚙️] │
│ AI-Enhanced ETL Platform                                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ 📊 AI Insights Overview                          🔄 Active Pipelines │
│ ┌─────────────────────────────┐                 ┌─────────────────────┐ │
│ │ 🧠 6 New Insights Generated │                 │ ✅ 3 Running       │ │
│ │ 📈 95% Data Quality Score   │                 │ ⏸️ 1 Paused        │ │
│ │ 🎯 $125K Revenue Predicted  │                 │ ❌ 0 Failed        │ │
│ │ [View All Insights]         │                 │ [Manage Pipelines] │ │
│ └─────────────────────────────┘                 └─────────────────────┘ │
│                                                                      │
│ 💬 Ask AI About Your Data                       📊 Recent Reports    │
│ ┌─────────────────────────────────────────────┐ ┌─────────────────────┐ │
│ │ [🎤] "What is the average price by category?" │ │ Executive Summary   │ │
│ │ [🔍 Ask Question]                           │ │ Sales Forecast      │ │
│ └─────────────────────────────────────────────┘ │ Quality Report      │ │
│                                                 │ [View All Reports]  │ │
│                                                 └─────────────────────┘ │
│                                                                      │
│ 🔮 Predictions & Forecasts                      ⚠️ Data Quality Alerts│
│ ┌─────────────────────────────┐                 ┌─────────────────────┐ │
│ │ 📈 Next 30 Days: +15% Sales│                 │ 🟡 2 Minor Issues   │ │
│ │ 📊 Inventory: Restock Soon  │                 │ 🟢 98.5% Complete   │ │
│ │ 🎯 Confidence: 87%         │                 │ [Review Issues]     │ │
│ │ [View Predictions]          │                 └─────────────────────┘ │
│ └─────────────────────────────┘                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Quick Actions Sidebar
```
┌─────────────────────┐
│ ⚡ Quick Actions    │
├─────────────────────┤
│ 🚀 Run AI Pipeline │
│ 📤 Upload Data      │
│ 📊 Generate Report  │
│ 🔍 Query Data       │
│ ⚙️ Schedule Job     │
│ 📈 View Analytics   │
└─────────────────────┘
```

## 🧠 AI Components Interface Wireframes

### AI Insights Generator Interface
```
┌─────────────────────────────────────────────────────────────────────┐
│ 🧠 AI Insights Generator                                   [⚙️Settings]│
├─────────────────────────────────────────────────────────────────────┤
│ Data Source: [Warehouse Products ▼] Records: 5,247    [🔄 Refresh]  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ 💡 Generated Insights (6 new)                                       │
│                                                                      │
│ ┌─────────────────────────────────────────────────────────────────┐   │
│ │ 🏷️ PRICING INSIGHT                          Confidence: 92% ⭐⭐⭐⭐⭐ │
│ │ Electronics category shows 15% price increase trend over 30 days │
│ │ Recommended Action: Review pricing strategy for competitive edge  │
│ │ [📊 View Details] [📤 Export] [❌ Dismiss]                      │
│ └─────────────────────────────────────────────────────────────────┘   │
│                                                                      │
│ ┌─────────────────────────────────────────────────────────────────┐   │
│ │ 📦 INVENTORY INSIGHT                         Confidence: 89% ⭐⭐⭐⭐ │
│ │ 23 products in Books category have low stock levels (<10 units)  │
│ │ Recommended Action: Initiate restock process for high-demand items│
│ │ [📊 View Details] [📤 Export] [❌ Dismiss]                      │
│ └─────────────────────────────────────────────────────────────────┘   │
│                                                                      │
│ [📊 Analytics Dashboard] [📈 Trend Analysis] [⚙️ Configure Insights] │
└─────────────────────────────────────────────────────────────────────┘
```

### AI Query Interface
```
┌─────────────────────────────────────────────────────────────────────┐
│ 💬 AI Query Interface - Natural Language Data Access               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ 🗣️ Ask me anything about your data...                              │
│ ┌─────────────────────────────────────────────────────────────────┐   │
│ │ What is the average price by category?                         │🎤│ │
│ │ [🔍 Ask Question] [🎲 Random Question] [📋 History]            │   │
│ └─────────────────────────────────────────────────────────────────┘   │
│                                                                      │
│ 🤖 AI Response:                                                     │
│ ┌─────────────────────────────────────────────────────────────────┐   │
│ │ Here are the average prices by category:                        │   │
│ │                                                                 │   │
│ │ 📱 Electronics: $186.45                                        │   │
│ │ 📚 Books: $18.32                                               │   │
│ │ 👕 Clothing: $42.18                                            │   │
│ │ 🏠 Home & Garden: $67.89                                       │   │
│ │                                                                 │   │
│ │ 📊 [View Chart] 📤 [Export Data] 🔄 [Refresh]                  │   │
│ │ 💡 Related Questions:                                           │   │
│ │ • Which category has the highest profit margin?                 │   │
│ │ • Show me top selling products in Electronics                   │   │
│ └─────────────────────────────────────────────────────────────────┘   │
│                                                                      │
│ 🕒 Recent Queries                            💡 Suggested Questions  │
│ • Average rating by category                 • Best performing products│
│ • Products with low stock                    • Sales trends this month│
│ • Top 10 expensive items                     • Customer satisfaction  │
└─────────────────────────────────────────────────────────────────────┘
```

### Predictive Analytics Dashboard
```
┌─────────────────────────────────────────────────────────────────────┐
│ 🔮 Predictive Analytics Engine                          [📅 30 Days ▼]│
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ 📈 Sales Forecast                                    📊 Trend Analysis│
│ ┌─────────────────────────────┐                     ┌─────────────────┐ │
│ │        $125,000            │                     │ 📈 Revenue: ↗15%│ │
│ │    Predicted Revenue       │                     │ 📦 Orders: ↗8%  │ │
│ │    Confidence: 87% ⭐⭐⭐⭐   │                     │ 🎯 Conversion:↗2%│ │
│ │                            │                     │ 📊 AOV: ↘3%     │ │
│ │ [📊 View Details]          │                     └─────────────────┘ │
│ └─────────────────────────────┘                                      │
│                                                                      │
│ 📊 Forecast Visualization                                            │
│ ┌─────────────────────────────────────────────────────────────────┐   │
│ │     Revenue Forecast (Next 30 Days)                            │   │
│ │ $   ┌─────────────────────────────────────────────────────────┐ │   │
│ │150K │                                      ╱╲                 │ │   │
│ │     │                                   ╱╱    ╲                │ │   │
│ │125K │                              ╱╱╱         ╲╲              │ │   │
│ │     │                         ╱╱╱╱                ╲╲╲          │ │   │
│ │100K │                   ╱╱╱╱╱                        ╲╲╲╲      │ │   │
│ │     │            ╱╱╱╱╱╱                                  ╲╲╲╲  │ │   │
│ │ 75K │     ╱╱╱╱╱╱                                            ╲╲ │ │   │
│ │     └─────────────────────────────────────────────────────────┘ │   │
│ │      Week 1   Week 2   Week 3   Week 4   Week 5               │   │
│ │      [━━━ Historical] [┅┅┅ Predicted] [▓▓▓ Confidence Range] │   │
│ └─────────────────────────────────────────────────────────────────┘   │
│                                                                      │
│ 🎯 Key Predictions                           ⚠️ Risk Factors         │
│ • Peak sales expected Week 3                • Market volatility: Med │
│ • Electronics category +20% growth          • Supply chain: Low risk │
│ • New customer acquisition: +12%            • Competition: High risk │
└─────────────────────────────────────────────────────────────────────┘
```

## 🔄 ETL Pipeline Management Interface

### Pipeline Overview
```
┌─────────────────────────────────────────────────────────────────────┐
│ ⚙️ ETL Pipeline Management                              [+ New Pipeline]│
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ 🔍 Filter: [All Pipelines ▼] [Status: Active ▼] [🔍 Search...]      │
│                                                                      │
│ Pipeline Name               Status    Last Run      Next Run    Actions│
│ ┌─────────────────────────────────────────────────────────────────┐   │
│ │🤖 AI Enhanced ETL DAG     ✅ Active   2 hrs ago    In 22 hrs  [▶️⏸️⚙️]│
│ │📊 Daily Sales Report      ✅ Active   6 hrs ago    In 18 hrs  [▶️⏸️⚙️]│
│ │🔍 Data Quality Check      🟡 Running  Running...   -          [⏹️👁️⚙️]│
│ │📈 Weekly Analytics        ⏸️ Paused   3 days ago   Paused     [▶️❌⚙️]│
│ │🧹 Data Cleanup           ❌ Failed    1 day ago    Disabled   [▶️🔄⚙️]│
│ └─────────────────────────────────────────────────────────────────┘   │
│                                                                      │
│ 📊 Pipeline Performance                          🔄 Recent Activities │
│ ┌─────────────────────────────┐                 ┌─────────────────────┐ │
│ │ Success Rate: 94.2%         │                 │ ✅ Sales ETL Complete│ │
│ │ Avg Duration: 12m 34s       │                 │ 🔄 Quality Check Run │ │
│ │ Total Runs Today: 8         │                 │ ⚠️ Cleanup Warning   │ │
│ │ [📈 View Trends]            │                 │ [View All Logs]     │ │
│ └─────────────────────────────┘                 └─────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### Pipeline Details View
```
┌─────────────────────────────────────────────────────────────────────┐
│ 🤖 AI Enhanced ETL DAG                                    [✏️ Edit]   │
├─────────────────────────────────────────────────────────────────────┤
│ Status: ✅ Running    Schedule: Daily @ 2:00 AM    Duration: ~15 min  │
│                                                                      │
│ 🔄 Pipeline Flow                                                     │
│ ┌─────────────────────────────────────────────────────────────────┐   │
│ │ [📥 Extract] → [🔍 Quality Check] → [🔄 Transform] → [📤 Load] │   │
│ │      ↓               ↓                   ↓             ↓        │   │
│ │ [🧠 AI Insights] → [📊 Generate Reports] → [📧 Notifications]   │   │
│ │                                                                 │   │
│ │ Task Status: 6/7 Complete ▓▓▓▓▓▓░                             │   │
│ │ Current: Generating AI Reports...                               │   │
│ └─────────────────────────────────────────────────────────────────┘   │
│                                                                      │
│ 📊 Execution History                             ⚙️ Configuration     │
│ ┌─────────────────────────────┐                 ┌─────────────────────┐ │
│ │ Date        Status   Duration│                 │ 🔄 Retry: 3 times  │ │
│ │ 2025-10-28  ✅ Success 14m   │                 │ ⏰ Timeout: 60m     │ │
│ │ 2025-10-27  ✅ Success 12m   │                 │ 📧 Alerts: Enabled  │ │
│ │ 2025-10-26  ⚠️ Warning  16m   │                 │ 🔄 Catchup: Disabled│ │
│ │ 2025-10-25  ✅ Success 11m   │                 │ [⚙️ Edit Settings]   │ │
│ └─────────────────────────────┘                 └─────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## 📊 Data Quality & Reports Interface

### Data Quality Dashboard
```
┌─────────────────────────────────────────────────────────────────────┐
│ 🔍 Smart Data Quality AI                                [🔄 Scan Now] │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ 📊 Overall Data Quality Score: 96.8% 🟢 Excellent                   │
│ ┌─────────────────────────────────────────────────────────────────┐   │
│ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░ 96.8%                                     │   │
│ └─────────────────────────────────────────────────────────────────┘   │
│                                                                      │
│ 📋 Quality Metrics                           ⚠️ Issues Found (3)     │
│ ┌─────────────────────────────┐                 ┌─────────────────────┐ │
│ │ ✅ Completeness: 98.5%      │                 │ 🟡 Minor: 2 issues │ │
│ │ ✅ Accuracy: 97.2%          │                 │ 🔴 Major: 1 issue  │ │
│ │ ✅ Consistency: 95.1%       │                 │ ❌ Critical: 0      │ │
│ │ ✅ Timeliness: 96.8%        │                 │ [🔧 Fix Issues]     │ │
│ └─────────────────────────────┘                 └─────────────────────┘ │
│                                                                      │
│ 🔍 Issue Details                                                     │
│ ┌─────────────────────────────────────────────────────────────────┐   │
│ │ 🟡 OUTLIER DETECTED                                             │   │
│ │ Product ID 1247: Price $9,999.99 exceeds normal range         │   │
│ │ Recommendation: Review pricing data for accuracy                │   │
│ │ [🔧 Fix] [👁️ Inspect] [❌ Ignore]                              │   │
│ └─────────────────────────────────────────────────────────────────┘   │
│                                                                      │
│ ┌─────────────────────────────────────────────────────────────────┐   │
│ │ 🟡 MISSING DATA                                                 │   │
│ │ 15 products missing category information (0.3% of dataset)     │   │
│ │ Recommendation: Auto-categorize using AI classification        │   │
│ │ [🤖 Auto-Fix] [✏️ Manual] [❌ Ignore]                          │   │
│ └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### AI Reports Generator
```
┌─────────────────────────────────────────────────────────────────────┐
│ 📊 AI Report Generator                               [+ New Report]  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│ 📋 Available Report Templates                                        │
│ ┌─────────────────────────────────────────────────────────────────┐   │
│ │ 🏢 Executive Summary          📊 Sales Analytics                │   │
│ │ • Key business metrics        • Revenue trends & forecasts      │   │
│ │ • AI-generated insights       • Product performance analysis    │   │
│ │ • Recommendations             • Customer behavior insights       │   │
│ │ [📄 Generate] [⚙️ Customize]   [📄 Generate] [⚙️ Customize]      │   │
│ │                                                                 │   │
│ │ 🔍 Data Quality Report        🔮 Predictive Analytics          │   │
│ │ • Quality score analysis      • Future sales predictions        │   │
│ │ • Issues and recommendations  • Market trend analysis           │   │
│ │ • Improvement suggestions     • Risk assessment                 │   │
│ │ [📄 Generate] [⚙️ Customize]   [📄 Generate] [⚙️ Customize]      │   │
│ └─────────────────────────────────────────────────────────────────┘   │
│                                                                      │
│ 📁 Recent Reports                                                    │
│ ┌─────────────────────────────────────────────────────────────────┐   │
│ │ Report Name              Generated        Size    Actions        │   │
│ │ Executive_Summary_Oct28  2 hours ago      2.4 MB  [👁️📤📋❌]    │   │
│ │ Sales_Analytics_Oct27    1 day ago        1.8 MB  [👁️📤📋❌]    │   │
│ │ Quality_Report_Oct26     2 days ago       945 KB  [👁️📤📋❌]    │   │
│ │ Predictive_Oct25         3 days ago       1.2 MB  [👁️📤📋❌]    │   │
│ └─────────────────────────────────────────────────────────────────┘   │
│                                                                      │
│ ⚙️ Report Configuration                      📊 Report Preview        │
│ • Date Range: Last 30 days                  [📊 Interactive Preview] │
│ • Include AI Insights: ✅ Yes               [🖼️ Visual Mockup]       │
│ • Export Format: PDF, HTML, Excel           [📱 Mobile View]         │
│ • Schedule: Manual / Daily / Weekly          [🖥️ Desktop View]        │
└─────────────────────────────────────────────────────────────────────┘
```

## 📱 Mobile Responsive Wireframes

### Mobile Dashboard
```
┌─────────────────────┐
│ ☰ GenETL        🔔⚙️│
├─────────────────────┤
│ Hi, User Name       │
│ AI ETL Platform     │
├─────────────────────┤
│ 🧠 AI Insights      │
│ ┌─────────────────┐ │
│ │ 6 New Insights  │ │
│ │ 95% Quality     │ │
│ │ $125K Predicted │ │
│ │ [View All]      │ │
│ └─────────────────┘ │
│                     │
│ 🔄 Active Pipelines │
│ ┌─────────────────┐ │
│ │ ✅ 3 Running    │ │
│ │ ⏸️ 1 Paused     │ │
│ │ ❌ 0 Failed     │ │
│ │ [Manage]        │ │
│ └─────────────────┘ │
│                     │
│ 💬 Ask AI           │
│ ┌─────────────────┐ │
│ │ "Average price  │ │
│ │ by category?"   │ │
│ │ [🎤 Ask]        │ │
│ └─────────────────┘ │
│                     │
│ 📊 Quick Reports    │
│ • Executive Summary │
│ • Sales Forecast    │
│ • Quality Report    │
│                     │
│ [📊][🔄][💬][📈][⚙️] │
└─────────────────────┘
```

## 🎨 Design System Components

### Color Palette
```
Primary Colors:
🔵 AI Blue (#017CEE)     - Trust, Intelligence, Primary Actions
🟢 Data Green (#28a745)  - Success, Growth, Positive Metrics
🟠 Insight Orange (#fd7e14) - Innovation, Warnings, Highlights

Secondary Colors:
⚫ Dark Navy (#1e2746)   - Text, Headers, Professional
⚪ Light Gray (#f8f9fa)  - Backgrounds, Cards, Subtle
🟡 Warning Amber (#ffc107) - Alerts, Attention, Cautions
```

### Typography Scale
```
H1: 32px Bold (Page Titles)
H2: 24px Bold (Section Headers)  
H3: 20px Bold (Card Titles)
H4: 16px Bold (Labels)
Body: 14px Regular (Main Text)
Small: 12px Regular (Metadata)
```

### Icon System
```
🧠 AI/Intelligence    🔄 Process/Pipeline    📊 Analytics/Charts
🔍 Search/Discovery   ⚙️ Settings/Config    📈 Growth/Trends
⚠️ Warnings/Alerts    ✅ Success/Complete   ❌ Error/Failed
💬 Communication      📤 Export/Share       🎯 Goals/Targets
```

### Component Specifications

**Cards**: 8px border radius, subtle shadow, white background
**Buttons**: Primary (AI Blue), Secondary (outline), Success (Data Green)
**Forms**: Clean inputs with labels, inline validation
**Tables**: Alternating row colors, sortable headers, action columns
**Charts**: Consistent color scheme, interactive tooltips, responsive
**Navigation**: Breadcrumbs, clear hierarchy, active states

## 📐 Layout Grid System

### Desktop Layout (1200px+)
- **Header**: 64px height
- **Sidebar**: 240px width (collapsible to 64px)
- **Main Content**: Fluid width with max 1140px
- **Grid**: 12-column system with 24px gutters

### Tablet Layout (768px - 1199px)
- **Header**: 56px height
- **Sidebar**: Overlay/drawer style
- **Main Content**: Full width with 16px margins
- **Grid**: 8-column system

### Mobile Layout (< 768px)
- **Header**: 48px height with hamburger menu
- **Navigation**: Bottom tab bar (5 main sections)
- **Content**: Single column, 16px margins
- **Cards**: Full width, stacked vertically

## 🔗 Interactive Elements

### Navigation Patterns
- **Breadcrumbs**: Home > AI Dashboard > Insights Generator
- **Tabs**: Horizontal tabs for related content sections
- **Filters**: Dropdown and toggle filters with clear/reset options
- **Pagination**: First/Prev/Numbers/Next/Last with page size options

### Data Visualization
- **Charts**: Interactive with hover details, zoom, and export
- **Tables**: Sortable columns, inline editing, bulk actions
- **Metrics Cards**: Large numbers with trend indicators
- **Progress Bars**: Completion status with percentages

### AI-Specific Elements
- **Confidence Indicators**: Star ratings or percentage with color coding
- **Chat Interface**: Conversational UI for AI Query Interface
- **Insight Cards**: Expandable cards with actions (dismiss, export, details)
- **Prediction Visualizations**: Forecast charts with confidence intervals

## 🎯 User Experience Flows

### New User Onboarding
1. **Welcome Screen**: Platform introduction and capabilities overview
2. **Data Source Setup**: Connect to existing databases or upload sample data
3. **First AI Analysis**: Guided tour through AI insights generation
4. **Pipeline Creation**: Set up first automated ETL pipeline
5. **Report Generation**: Create first business intelligence report

### Daily User Journey
1. **Dashboard Overview**: Check AI insights and pipeline status
2. **Query Interface**: Ask questions about data in natural language
3. **Review Alerts**: Address any data quality or pipeline issues
4. **Generate Reports**: Create and share business intelligence reports
5. **Monitor Performance**: Track pipeline success and system health

### Admin Configuration Flow
1. **System Settings**: Configure database connections and security
2. **User Management**: Set up roles and permissions
3. **Pipeline Templates**: Create reusable ETL workflow templates
4. **Monitoring Setup**: Configure alerts and performance monitoring
5. **Backup Configuration**: Set up automated backup procedures

## 📋 Accessibility Requirements

### WCAG 2.1 AA Compliance
- **Color Contrast**: Minimum 4.5:1 ratio for normal text
- **Keyboard Navigation**: Full functionality without mouse
- **Screen Reader**: Proper ARIA labels and semantic HTML
- **Focus Indicators**: Clear visual focus states
- **Alternative Text**: Descriptive alt text for all images/charts

### Responsive Design
- **Flexible Layouts**: Adapt to different screen sizes
- **Touch Targets**: Minimum 44px for mobile interactions
- **Readable Text**: Scalable fonts, minimum 16px on mobile
- **Orientation**: Support both portrait and landscape modes

## 🚀 Technical Implementation Notes

### Frontend Framework Suggestions
- **React** with TypeScript for type safety
- **Material-UI** or **Ant Design** for consistent components
- **D3.js** or **Chart.js** for data visualizations
- **React Query** for API state management

### Performance Considerations
- **Lazy Loading**: Load AI insights and reports on demand
- **Virtual Scrolling**: Handle large data tables efficiently  
- **Caching**: Cache API responses and computed visualizations
- **Progressive Enhancement**: Core functionality works without JavaScript

### Security Features
- **Role-Based Access**: Different views for different user types
- **Data Masking**: Hide sensitive information from unauthorized users
- **Audit Logging**: Track all user actions and data access
- **Session Management**: Automatic logout and session validation

---

## 📝 Wireframe Deliverables Checklist

When creating wireframes, ensure you include:

### Main Interfaces
- [ ] Dashboard/Home page with AI overview
- [ ] AI Insights Generator interface
- [ ] AI Query Interface (natural language)
- [ ] Predictive Analytics dashboard
- [ ] ETL Pipeline management
- [ ] Data Quality monitoring
- [ ] Report Generator interface

### User Management
- [ ] Login/authentication screens
- [ ] User profile and settings
- [ ] Admin user management
- [ ] Role-based permission views

### Data Management
- [ ] Data source configuration
- [ ] Database connection setup
- [ ] File upload interface
- [ ] Data preview and validation

### Responsive Views
- [ ] Desktop layouts (1200px+)
- [ ] Tablet layouts (768-1199px)
- [ ] Mobile layouts (<768px)
- [ ] Navigation adaptations

### Interactive States
- [ ] Loading states for AI processing
- [ ] Error states and recovery options
- [ ] Empty states with helpful guidance
- [ ] Success confirmations

### Documentation
- [ ] Component specifications
- [ ] Color and typography guide
- [ ] Icon library and usage
- [ ] Interaction patterns

---

**🎨 Design Tools Recommended:**
- Figma (preferred for collaboration)
- Sketch + InVision
- Adobe XD
- Balsamiq (for low-fidelity wireframes)

**📱 Device Testing:**
- iPhone 13/14 (390x844px)
- Samsung Galaxy S21 (384x854px)  
- iPad Air (820x1180px)
- Desktop 1920x1080px
- Desktop 1440x900px

This comprehensive wireframe prompt should provide everything needed to create professional, user-friendly interfaces for the GenETL AI-Enhanced ETL platform!