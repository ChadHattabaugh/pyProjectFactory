# GitHub Project Setup Guide

This guide explains how to set up GitHub Projects for roadmap visualization and project management.

## 🎯 **Setting Up GitHub Projects**

### **Step 1: Create New Project**
1. Go to your repository → **Projects** tab
2. Click **"New Project"**
3. Choose **"Table"** view initially
4. Name: "pyProjectTemplate Roadmap"

### **Step 2: Add Roadmap View**
1. Click **"+ New view"** 
2. Select **"Roadmap"** layout
3. Name: "Development Roadmap"
4. Set zoom level to **"Quarter"** for strategic view

### **Step 3: Configure Custom Fields**

#### **Required Fields:**
- **Status**: Single select
  - 📋 Planning
  - 🔄 In Progress  
  - ✅ Complete
  - 🚫 Blocked
  - ❄️ On Hold

- **Priority**: Single select
  - 🔥 Critical
  - ⚡ High
  - 📈 Medium
  - 📉 Low

- **Effort**: Single select
  - 🟢 Small (1-3 days)
  - 🟡 Medium (1-2 weeks)
  - 🟠 Large (2-4 weeks)
  - 🔴 X-Large (1+ months)

- **Target Quarter**: Single select
  - Q4 2025
  - Q1 2025
  - Q2 2025
  - Future

- **Start Date**: Date field
- **Target Date**: Date field

### **Step 4: Create Milestones**
Set up repository milestones that align with roadmap phases:

1. **v0.2.0 - Configuration System** (Q4 2025)
2. **v0.3.0 - FastAPI Templates** (Q1 2025)
3. **v0.4.0 - Template Ecosystem** (Q2 2025)
4. **v0.5.0 - AI Enhancement** (Q2 2025)

### **Step 5: Link Issues to Project**

#### **Existing Issues to Add:**
- #14: Use a project setup yaml to serve user input
- #15: Read config when running project_setup.py  
- #16: Write responses to a project_setup.yaml
- #17: Document a basic project_setup.yaml template
- #13: CODEOWNERS integration
- #8: FastAPI project templates

#### **Set Field Values:**
```
Issue #14-17 (YAML Config):
- Status: Planning
- Priority: High
- Effort: Medium  
- Target Quarter: Q4 2025
- Milestone: v0.2.0

Issue #13 (CODEOWNERS):
- Status: Planning
- Priority: Medium
- Effort: Small
- Target Quarter: Q4 2025
- Milestone: v0.2.1

Issue #8 (FastAPI):
- Status: Planning  
- Priority: High
- Effort: Large
- Target Quarter: Q1 2025
- Milestone: v0.3.0
```

### **Step 6: Configure Roadmap Display**

#### **Roadmap Settings:**
- **Zoom Level**: Quarter (for strategic overview)
- **Date Range**: 12 months from current date
- **Grouping**: Group by milestone or status
- **Markers**: Show milestones and target dates

#### **Swimlanes** (Optional):
- Group by **Priority** to show critical items at top
- Group by **Area** (setup, template, ci/cd, docs)

### **Step 7: Automation (Optional)**

#### **Auto-Add Issues:**
Set up automation to automatically add new issues to project:
1. Project Settings → **Workflows**
2. **"Item added to project"** trigger
3. **Actions**: Set default status to "Planning"

#### **Status Transitions:**
- When PR linked → Status: "In Progress"  
- When PR merged → Status: "Complete"
- When issue closed → Archive item

## 📊 **Using the Roadmap**

### **Strategic Planning**
- **Quarterly View**: High-level feature planning
- **Milestone Tracking**: Progress toward releases
- **Dependency Visualization**: See feature relationships

### **Sprint Planning**
- **Monthly View**: Detailed sprint planning
- **Effort Estimation**: Plan team capacity
- **Priority Ordering**: Focus on high-impact items

### **Stakeholder Communication**
- **Visual Timeline**: Share roadmap with stakeholders
- **Progress Updates**: Show completed vs planned work
- **Scope Changes**: Drag and drop to adjust timelines

## 🎯 **Best Practices**

### **Keep It Strategic**
- Focus on features, not individual bugs
- Use epics for complex features
- Link detailed work items as subtasks

### **Regular Updates**
- Review roadmap monthly
- Update progress and timelines
- Archive completed items

### **Team Collaboration**
- Use project discussions for planning
- Tag team members in roadmap items
- Link to detailed design documents

### **Communication**
- Share roadmap view URL with stakeholders
- Export roadmap for presentations
- Use project insights for progress reports

## 🔗 **Integration with Issues**

### **Issue Templates**
Create issue templates that include roadmap fields:
```markdown
## Roadmap Information
- **Priority**: [Critical/High/Medium/Low]
- **Effort**: [Small/Medium/Large/X-Large]  
- **Target Quarter**: [Q4 2025/Q1 2025/Q2 2025]
- **Dependencies**: [List any blocking issues]
```

### **Label Integration**
Use consistent labels that map to project fields:
- `priority: high` → High priority in project
- `effort: large` → Large effort in project
- `area: template` → Template area grouping

This creates a seamless workflow between issue management and roadmap planning.