from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import schemas, models, security, database

router = APIRouter(prefix="/transactions", tags=["Transactions"])

from sqlalchemy.orm import selectinload

@router.post("/deposit", response_model=schemas.UserResponse)
async def deposit(
    transaction: schemas.TransactionCreate,
    current_user: models.User = Depends(security.get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    user_id = current_user.id # Cache ID before commit expires the instance
    
    current_user.balance += transaction.amount
    
    new_transaction = models.Transaction(
        amount=transaction.amount,
        type="deposit",
        user_id=user_id
    )
    
    db.add(new_transaction)
    await db.commit()
    
    # Reload user with transactions to satisfy response model
    stmt = select(models.User).options(selectinload(models.User.transactions)).where(models.User.id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()

@router.post("/withdraw", response_model=schemas.UserResponse)
async def withdraw(
    transaction: schemas.TransactionCreate,
    current_user: models.User = Depends(security.get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    if current_user.balance < transaction.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    user_id = current_user.id # Cache ID before commit expires the instance
    
    current_user.balance -= transaction.amount
    
    new_transaction = models.Transaction(
        amount=transaction.amount,
        type="withdraw",
        user_id=user_id
    )
    
    db.add(new_transaction)
    await db.commit()
    
    stmt = select(models.User).options(selectinload(models.User.transactions)).where(models.User.id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()

@router.get("/statement", response_model=schemas.UserResponse)
async def get_statement(
    current_user: models.User = Depends(security.get_current_user),
    db: AsyncSession = Depends(database.get_db)
):
    # Depending on how the relationship is loaded (lazy by default), accessing current_user.transactions might fail in async context if not joined.
    # Let's perform a query with join or selectinload
    from sqlalchemy.orm import selectinload
    
    stmt = select(models.User).options(selectinload(models.User.transactions)).where(models.User.id == current_user.id)
    result = await db.execute(stmt)
    user_with_transactions = result.scalars().first()
    
    return user_with_transactions
